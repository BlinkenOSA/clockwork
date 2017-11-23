# coding: utf-8
import mysql.connector
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.conf import settings
from django.db import IntegrityError
from hashids import Hashids

from authority.models import Language, Genre
from container.models import Container
from controlled_list.models import Locale, DateType, LanguageUsage, PrimaryType
from finding_aids.models import FindingAidsEntity, FindingAidsEntityDate, FindingAidsEntityLanguage
from migration.management.commands.common_functions import get_approx_date


class Command(BaseCommand):
    help = 'Migrate ContentAV.'
    cnx = mysql.connector.connect(user=settings.MIGRATION_DB['USER'],
                                  password=settings.MIGRATION_DB['PASSWORD'],
                                  host=settings.MIGRATION_DB['HOST'],
                                  database='clkwrk_import_contents')

    def handle(self, *args, **options):
        FindingAidsEntity.objects.filter(primary_type=PrimaryType.objects.get(type='Video')).delete()
        FindingAidsEntity.objects.filter(primary_type=PrimaryType.objects.get(type='Audio')).delete()

        if settings.MIGRATION_DB:
            sql = "SELECT ContentsAV.*, Main.FondsID, Main.SubfondsID, Main.SeriesID, Main.ListNo, Main.Container, " \
                  "       ListsInSeries.DatePublic " \
                  "FROM ContentsAV INNER JOIN Main ON ContentsAV.ContainerID = Main.ID " \
                  "INNER JOIN ListsInSeries ON Main.FondsID = ListsInSeries.FondsID AND " \
                  "                            Main.SubfondsID = ListsInSeries.SubfondsID AND " \
                  "                            Main.SeriesID = ListsInSeries.SeriesID AND " \
                  "                            Main.ListNo = ListsInSeries.ListNo " \
                  "WHERE Main.ListNo = 1 AND " \
                  "(YearAir IS NOT NULL OR YearProduction IS NOT NULL)" \
                  "ORDER BY Main.FondsID, Main.SubfondsID, Main.SeriesID, Main.ListNo, Main.Container, ContentsAV.`No`"

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
                    # Title
                    if row['Title2']:
                        title_original = row['Title']
                        title = row['Title2']
                    else:
                        title_original = ""
                        title = row['Title']

                    if row['SequenceInformation']:
                        title = "%s %s" % (title, row['SequenceInformation'])
                        title_original = "%s %s" % (title_original, row['SequenceInformation'])

                    # Date
                    if row['YearProduction']:
                        date_from = get_approx_date(row['YearProduction'], row['MonthProduction'], row['DayProduction'])
                    else:
                        date_from = get_approx_date(row['YearAir'], row['MonthAir'], row['DayAir'])

                    user = User.objects.get(username='finding.aids')
                    hashids = Hashids(salt="osacontent", min_length=8)

                    finding_aids = FindingAidsEntity(
                        old_id="%s-%d" % (row['ContainerID'], int(row['No'])),
                        catalog_id=hashids.encode(row["ContainerID"] * 1000 + int(row["No"])),
                        archival_unit=container.archival_unit,
                        container=container,
                        primary_type=container.primary_type,
                        level='F',
                        is_template=False,
                        folder_no=folder_no,
                        title=title,
                        title_original=title_original,
                        contents_summary=row['Description'],
                        date_from=date_from,
                        note=row['Notes'],
                        time_start=self.get_timedelta(row['TimeStart']),
                        time_end=self.get_timedelta(row['TimeEnd']),
                        duration=self.get_timedelta(row['Duration']),
                        published=True if row['DatePublic'] else False,
                        date_published=row['DatePublic'] if row['DatePublic'] else None,
                        user_created=user.username,
                        user_updated=user.username
                    )

                    if FindingAidsEntity.objects.filter(container=container, folder_no=folder_no).count() == 0:
                        try:
                            finding_aids.save()
                            print("Inserting %s/%s:%s" % (finding_aids.archival_unit.reference_code,
                                                          container.container_no,
                                                          finding_aids.folder_no))

                            if row['YearAir']:
                                FindingAidsEntityDate.objects.create(
                                    fa_entity=finding_aids,
                                    date_from=get_approx_date(row['YearAir'], row['MonthAir'], row['DayAir']),
                                    date_type=DateType.objects.get(type='Date of Air')
                                ).save()

                            if row['YearProduction']:
                                FindingAidsEntityDate.objects.create(
                                    fa_entity=finding_aids,
                                    date_from=get_approx_date(row['YearProduction'],
                                                              row['MonthProduction'],
                                                              row['DayProduction']),
                                    date_type=DateType.objects.get(type='Date of Production')
                                ).save()

                            if row['ProgramTypeID']:
                                genre, created = Genre.objects.get_or_create(genre=self.get_genre(row['ProgramTypeID']))
                                finding_aids.genre.add(genre)
                                finding_aids.save()

                            languages = self.get_languages(row['LanguageID'], row['ContainerID'], row['No'])
                            for language in languages:
                                FindingAidsEntityLanguage.objects.create(
                                    fa_entity=finding_aids,
                                    language=language[0],
                                    language_usage=language[1]
                                ).save()

                            if row['Description2']:
                                finding_aids.original_locale = Locale.objects.get(pk='HU')
                                finding_aids.contents_summary_original = row['Description2']
                                finding_aids.save()

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

    def get_genre(self, genre):
        if genre:
            sql_prg_types = "SELECT * FROM ProgramTypes WHERE ID = %s"
            cursor = self.cnx.cursor(dictionary=True, buffered=True)

            cursor.execute(sql_prg_types, (genre,))
            rec = cursor.fetchone()
            return rec['ProgramType']
        else:
            return genre

    def get_languages(self, language_id, container_id, entry_no):
        lang = []

        sql_language = "SELECT iso_code FROM Languages WHERE ID = %s"
        sql_languages = "SELECT LanguagesInEntries.ContainerId, " \
                        "       LanguagesInEntries.EntryNo, " \
                        "       Languages.iso_code, " \
                        "       osaLanguageUses.LanguageUse " \
                        "FROM LanguagesInEntries " \
                        "INNER JOIN Languages ON LanguagesInEntries.LanguageId = Languages.ID " \
                        "INNER JOIN osaLanguageUses ON LanguagesInEntries.UseId = osaLanguageUses.Id " \
                        "WHERE ContainerId = %s AND EntryNo = %s"

        cursor_one = self.cnx.cursor(buffered=True, dictionary=True)
        cursor_two = self.cnx.cursor(buffered=True, dictionary=True)

        cursor_one.execute(sql_language, (language_id, ))
        cursor_two.execute(sql_languages, (container_id, entry_no))

        main_language = cursor_one.fetchone()
        if main_language:
            main_language = main_language['iso_code']
            l = Language.objects.filter(iso_639_2=main_language).first()
            if l:
                lang.append([l, LanguageUsage.objects.get(usage='Original')])
            else:
                print('Missing language code: %s' % main_language)

        for row in cursor_two:
            l = Language.objects.filter(iso_639_2=row['iso_code']).first()
            lu = LanguageUsage.objects.filter(usage=row['LanguageUse']).first()
            if l and lu:
                lang.append([l, lu])
            else:
                print('Missing language code: %s (%s)' % (row['iso_code'], row['LanguageUse']))

        return lang

    def get_timedelta(self, date):
        if date:
            return timedelta(hours=date.hour, minutes=date.minute, seconds=date.second)
        else:
            return date
