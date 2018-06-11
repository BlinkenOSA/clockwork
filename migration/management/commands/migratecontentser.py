# coding: utf-8
import mysql.connector

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.conf import settings
from django.db import IntegrityError
from hashids import Hashids

from container.models import Container
from controlled_list.models import PrimaryType
from finding_aids.models import FindingAidsEntity, FindingAidsEntityAlternativeTitle
from migration.management.commands.common_functions import get_approx_date, get_approx_date_from_string


class Command(BaseCommand):
    help = 'Migrate ContentER.'
    cnx = mysql.connector.connect(user=settings.MIGRATION_DB['USER'],
                                  password=settings.MIGRATION_DB['PASSWORD'],
                                  host=settings.MIGRATION_DB['HOST'],
                                  database=settings.MIGRATION_DB['DB'])

    def handle(self, *args, **options):
        if settings.MIGRATION_DB:
            sql = "SELECT ContentsER.*, Main.FondsID, Main.SubfondsID, Main.SeriesID, Main.ListNo, Main.Container, " \
                  "       ListsInSeries.DatePublic " \
                  "FROM ContentsER INNER JOIN Main ON ContentsER.ContainerID = Main.ID " \
                  "INNER JOIN ListsInSeries ON Main.FondsID = ListsInSeries.FondsID AND " \
                  "                            Main.SubfondsID = ListsInSeries.SubfondsID AND " \
                  "                            Main.SeriesID = ListsInSeries.SeriesID AND " \
                  "                            Main.ListNo = ListsInSeries.ListNo " \
                  "WHERE Main.ListNo = 1 " \
                  "ORDER BY Main.FondsID, Main.SubfondsID, Main.SeriesID, Main.ListNo, Main.Container, ContentsER.`No`"

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
                    title = row['Description']

                    user = User.objects.get(username='finding.aids')
                    hashids = Hashids(salt="osacontent", min_length=8)

                    finding_aids, created = FindingAidsEntity.objects.get_or_create(
                        old_id="%s-%d" % (row['ContainerID'], int(row['No'])),
                        archival_unit=container.archival_unit,
                        container=container,
                    )

                    finding_aids.catalog_id = hashids.encode(row["ContainerID"] * 1000 + int(row["No"]))
                    finding_aids.primary_type = PrimaryType.objects.get(type='Electronic Record')
                    finding_aids.level = 'F'
                    finding_aids.is_template = False
                    finding_aids.folder_no = folder_no
                    finding_aids.title = title
                    finding_aids.date_from = get_approx_date(row['YearStart'], row['MonthStart'], row['DayStart'])
                    finding_aids.date_to = get_approx_date(row['YearEnd'], row['MonthEnd'], row['DayEnd'])
                    finding_aids.date_ca_span = row['CircaSpan'] if row['CircaSpan'] else 0
                    finding_aids.note = row['Notes']
                    finding_aids.published = True if row['DatePublic'] else False
                    finding_aids.date_published = row['DatePublic'] if row['DatePublic'] else None
                    finding_aids.user_created = user.username
                    finding_aids.user_updated = user.username

                    try:
                        finding_aids.save()
                    except IntegrityError as e:
                            print('Error with %s/%s:%s - %s' % (finding_aids.archival_unit.reference_code,
                                                                container.container_no,
                                                                finding_aids.folder_no,
                                                                e.args[1]))

                else:
                    print('Container not found! - %s-%s' % (ref_code, int(row['No']))
)

            self.cnx.close()
        else:
            print("Missing 'migration' database setting in 'settings.py'")
