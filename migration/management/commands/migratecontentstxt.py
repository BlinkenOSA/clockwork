# coding: utf-8
import mysql.connector
from datetime import datetime

import pytz
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.conf import settings
from django.db import IntegrityError
from hashids import Hashids
from pytz import timezone

from archival_unit.models import ArchivalUnit
from authority.models import Language
from container.models import Container
from controlled_list.models import Locale, AccessRight, ReproductionRight, PrimaryType
from finding_aids.models import FindingAidsEntity, FindingAidsEntityAlternativeTitle
from isaar.models import Isaar, IsaarStandardizedName, IsaarOtherName, IsaarParallelName
from isad.models import Isad
from migration.management.commands.common_functions import get_user, get_approx_date, get_approx_date_from_string


class Command(BaseCommand):
    help = 'Migrate ContentTXT.'
    cnx = mysql.connector.connect(user=settings.MIGRATION_DB['USER'],
                                  password=settings.MIGRATION_DB['PASSWORD'],
                                  host=settings.MIGRATION_DB['HOST'],
                                  database=settings.MIGRATION_DB['DB'])

    def add_arguments(self, parser):
        parser.add_argument('--fonds', dest='fonds', help='Fonds Number')
        parser.add_argument('--subfonds', dest='subfonds', help='Subfonds Number')
        parser.add_argument('--series', dest='series', help='Series Number')
        parser.add_argument('--container_list', dest='container_list', help='Container List')

    def handle(self, *args, **options):
        where = []
        if options['fonds']:
            where.append("Main.FondsID = %s" % options['fonds'])
        if options['subfonds']:
            where.append("Main.SubfondsID = %s" % options['subfonds'])
        if options['series']:
            where.append("Main.SeriesID = %s" % options['series'])

        if options['container_list']:
            where.append("Main.ListNo = %s" % options['container_list'])
        else:
            where.append("Main.ListNo = 1")

        where = " AND ".join(where)

        if settings.MIGRATION_DB:
            sql = "SELECT Contents.*, Main.FondsID, Main.SubfondsID, Main.SeriesID, Main.ListNo, Main.Container, " \
                  "       ListsInSeries.DatePublic " \
                  "FROM Contents INNER JOIN Main ON Contents.ContainerID = Main.ID " \
                  "INNER JOIN ListsInSeries ON Main.FondsID = ListsInSeries.FondsID AND " \
                  "                            Main.SubfondsID = ListsInSeries.SubfondsID AND " \
                  "                            Main.SeriesID = ListsInSeries.SeriesID AND " \
                  "                            Main.ListNo = ListsInSeries.ListNo "

            sql = sql + "WHERE " + where + \
                " ORDER BY Main.FondsID, Main.SubfondsID, Main.SeriesID, Main.ListNo, Main.Container, Contents.`No`"

            cursor = self.cnx.cursor(dictionary=True, buffered=True)
            cursor.execute(sql)

            container_no = 0
            folder_no = 0
            ref_code = "0-0-0"

            for row in cursor:
                ref_code_current = "%s-%s-%s" % (row['FondsID'], row['SubfondsID'], row['SeriesID'])
                if ref_code_current == ref_code:
                    if int(row['Container']) == container_no:
                        folder_no += 1
                    if int(row['Container']) != container_no:
                        container_no = int(row['Container'])
                        folder_no = 1
                else:
                    ref_code = ref_code_current
                    container_no = 1
                    folder_no = 1

                container = Container.objects.filter(old_id=row['ContainerID']).first()

                if container:
                    if row['SequenceInformation']:
                        title = "%s %s" % (row['Description'], row['SequenceInformation'])
                    else:
                        title = row['Description']

                    user = User.objects.get(username='finding.aids')
                    hashids = Hashids(salt="osacontent", min_length=8)

                    finding_aids = FindingAidsEntity(
                        old_id="%s-%d" % (row['ContainerID'], int(row['No'])),
                        catalog_id=hashids.encode(row["ContainerID"] * 1000 + int(row["No"])),
                        archival_unit=container.archival_unit,
                        container=container,
                        primary_type=PrimaryType.objects.get(type='Text'),
                        level='F',
                        is_template=False,
                        folder_no=folder_no,
                        title=title,
                        date_from=get_approx_date(row['YearStart'], row['MonthStart'], row['DayStart']),
                        date_to=get_approx_date(row['YearEnd'], row['MonthEnd'], row['DayEnd']),
                        date_ca_span=row['CircaSpan'] if row['CircaSpan'] else 0,
                        note=row['Notes'],
                        published=True if row['DatePublic'] else False,
                        date_published=row['DatePublic'] if row['DatePublic'] else None,
                        user_created=user.username,
                        user_updated=user.username
                    )

                    if FindingAidsEntity.objects.filter(container=container, folder_no=folder_no).count() == 0:
                        try:
                            finding_aids.save()
                            # print("Inserting %s/%s:%s" % (finding_aids.archival_unit.reference_code,
                            #                               container.container_no,
                            #                               finding_aids.folder_no))
                            if row['TranslatedTitle']:
                                fa_at = FindingAidsEntityAlternativeTitle(
                                    fa_entity=finding_aids,
                                    alternative_title=row['TranslatedTitle']
                                )
                                fa_at.save()

                            if row['TransliteratedTitle']:
                                fa_at = FindingAidsEntityAlternativeTitle(
                                    fa_entity=finding_aids,
                                    alternative_title=row['TransliteratedTitle']
                                )
                                fa_at.save()

                        except IntegrityError as e:
                                print('Error with %s/%s:%s - %s' % (finding_aids.archival_unit.reference_code,
                                                                    container.container_no,
                                                                    finding_aids.folder_no,
                                                                    e.args[1]))
                    else:
                        print("Already exists %s/%s:%s" % (finding_aids.archival_unit.reference_code,
                                                           container.container_no,
                                                           finding_aids.folder_no))

                else:
                    print('Container not found!')

            self.cnx.close()
        else:
            print("Missing 'migration' database setting in 'settings.py'")
