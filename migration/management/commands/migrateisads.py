# coding: utf-8
import mysql.connector
from datetime import datetime

import pytz
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.conf import settings
from django.db import IntegrityError
from pytz import timezone

from archival_unit.models import ArchivalUnit
from authority.models import Language
from controlled_list.models import Locale, AccessRight, ReproductionRight
from isaar.models import Isaar, IsaarStandardizedName, IsaarOtherName, IsaarParallelName
from isad.models import Isad
from migration.management.commands.common_functions import get_user, get_approx_date, get_approx_date_from_string


class Command(BaseCommand):
    help = 'Migrate ISAD(G) Records.'
    cnx = mysql.connector.connect(user=settings.MIGRATION_DB['USER'],
                                  password=settings.MIGRATION_DB['PASSWORD'],
                                  host=settings.MIGRATION_DB['HOST'],
                                  database=settings.MIGRATION_DB['DB'])

    def handle(self, *args, **options):
        if settings.MIGRATION_DB:
            self.migrate_isad_fonds()
            self.migrate_isad_subfonds()
            self.migrate_isad_series()
            self.cnx.close()
        else:
            print("Missing 'migration' database setting in 'settings.py'")

    def migrate_isad_fonds(self):
            sql = "SELECT fonds.ID AS fondsID, fonds.Name AS ArchivalUnitName, isad.* " \
                  "FROM fonds " \
                  "INNER JOIN isad ON fonds.isadId = isad.Id " \
                  "ORDER BY FondsID"

            cursor = self.cnx.cursor(dictionary=True, buffered=True)
            cursor.execute(sql)

            for row in cursor:
                archival_unit = ArchivalUnit.objects.filter(level='F', fonds=row['fondsID']).first()

                isad = self.make_isad_record(archival_unit, row)

                try:
                    isad.save()
                    print("Inserting %s" % archival_unit.title_full)
                    self.add_isad_languages(isad)

                except IntegrityError as e:
                    print('Error with %s: %s' % (archival_unit.title_full.encode('utf-8'), e.args[1]))

    def migrate_isad_subfonds(self):
            sql = "SELECT subfonds.ID AS subfondsID, subfonds.FondsID AS fondsID, subfonds.Name AS ArchivalUnitName, isad.* " \
                  "FROM subfonds " \
                  "INNER JOIN isad ON subfonds.isadId = isad.Id " \
                  "ORDER BY FondsID, SubfondsID"

            cursor = self.cnx.cursor(dictionary=True, buffered=True)
            cursor.execute(sql)

            for row in cursor:
                archival_unit = ArchivalUnit.objects.filter(level='SF',
                                                            fonds=row['fondsID'],
                                                            subfonds=row['subfondsID']).first()

                isad = self.make_isad_record(archival_unit, row)

                try:
                    isad.save()
                    print("Inserting %s" % archival_unit.title_full)
                    self.add_isad_languages(isad)

                except IntegrityError as e:
                    print('Error with %s: %s' % (archival_unit.title_full.encode('utf-8'), e.args[1]))

    def migrate_isad_series(self):
            sql = "SELECT series.ID AS seriesID, series.subfondsID AS subfondsID, series.FondsID AS fondsID, " \
                  "series.Name AS ArchivalUnitName, isad.* " \
                  "FROM series " \
                  "INNER JOIN isad ON series.isadId = isad.Id " \
                  "ORDER BY FondsID, SubfondsID, SeriesID"

            cursor = self.cnx.cursor(dictionary=True, buffered=True)
            cursor.execute(sql)

            for row in cursor:
                archival_unit = ArchivalUnit.objects.filter(level='S',
                                                            fonds=row['fondsID'],
                                                            subfonds=row['subfondsID'],
                                                            series=row['seriesID']).first()

                isad = self.make_isad_record(archival_unit, row)

                try:
                    isad.save()
                    print("Inserting %s" % archival_unit.title_full)
                    self.add_isad_languages(isad)

                except IntegrityError as e:
                    print('Error with %s: %s' % (archival_unit.title_full.encode('utf-8'), e.args[1]))

    def make_isad_record(self, archival_unit, row):
        sql_isad2 = "SELECT * FROM isad2 WHERE isad2.Id = %s"

        cursor = self.cnx.cursor(dictionary=True, buffered=True)
        cursor.execute(sql_isad2, (row['Id'],))

        isad2 = cursor.fetchone()

        tz_budapest = timezone('Europe/Budapest')
        original_locale = Locale.objects.get(pk='HU')

        updated_by = get_user(row['Last edited by']).username
        last_edited = tz_budapest.localize(row['Last edited']) if row['Last edited'] else datetime.now(tz_budapest)

        access_rights = row['Conditions governing access']
        reproduction_rights = row['Conditions governing reproduction']

        isad = Isad(
            legacy_id=row['Id'],
            archival_unit=archival_unit,
            original_locale=original_locale,
            title=row['ArchivalUnitName'],
            reference_code=archival_unit.reference_code,
            description_level=archival_unit.level,
            year_from=row['YearFrom'],
            year_to=row['YearTo'],
            accruals=True if row['Accruals'] == 'Expected' else False,
            access_rights=AccessRight.objects.filter(statement='Unknown').first() if not access_rights else None,
            access_rights_legacy=access_rights,
            reproduction_rights=ReproductionRight.objects.filter(
                statement='Third party rights are to be cleared.').first() if not reproduction_rights else None,
            reproduction_rights_legacy=reproduction_rights,
            date_predominant=row['Date(s)'],
            carrier_estimated=row['Extent and medium'],
            archival_history=row['Archival history'],
            archival_history_original=isad2['Archival history'] if isad2 else "",
            scope_and_content_abstract=row['Scope and content'],
            scope_and_content_abstract_original=isad2['Scope and content'] if isad2 else "",
            appraisal=row['Appraisal, destruction and scheduling information'],
            appraisal_original=isad2['Appraisal, destruction and scheduling information'] if isad2 else "",
            system_of_arrangement_information=row['System of arrangement'],
            system_of_arrangement_information_original=isad2['System of arrangement'] if isad2 else "",
            physical_characteristics=row['Physical characteristics and technical requirements'],
            physical_characteristics_original=isad2['Physical characteristics and technical requirements'] if isad2 else "",
            publication_note=row['Publication note'],
            publication_note_original=isad2['Publication note'] if isad2 else "",
            note=row['Note'],
            note_original=isad2['Note'] if isad2 else "",
            internal_note=row['Internal notes'],
            internal_note_original=isad2['Internal notes'] if isad2 else "",
            archivists_note=row["Archivist's Note"],
            archivists_note_original=isad2["Archivist's Note"] if isad2 else "",
            published=True if row['DatePublic'] else False,
            user_published=updated_by,
            date_published=last_edited,
            user_created=User.objects.get(username='finding.aids').username,
            date_created=last_edited,
            user_updated=updated_by,
            date_updated=last_edited,
        )
        return isad

    def add_isad_languages(self, isad):
        sql_language = "SELECT languagesinisad.IsadId, Languages.* FROM Languages " \
                       "INNER JOIN languagesinisad ON languagesinisad.LanguageId = Languages.ID " \
                       "WHERE languagesinisad.IsadId = %s AND iso_code IS NOT NULL"

        cursor = self.cnx.cursor(dictionary=True, buffered=True)
        cursor.execute(sql_language, (isad.legacy_id,))

        for row in cursor:
            language = Language.objects.filter(iso_639_2=row['iso_code']).first()
            if language:
                isad.language.add(language)
            else:
                print("I can't find equivalent for the language: %s" % row['Language'])
        isad.save()
