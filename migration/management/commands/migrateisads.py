# coding: utf-8
import mysql.connector
from datetime import datetime

import pytz
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.conf import settings
from django.db import IntegrityError
from django.db.models import Q
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
                if archival_unit:
                    isad = self.make_isad_record(archival_unit, row)

                    try:
                        isad.save()
                        # print("Inserting %s" % archival_unit.title_full)
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

                if archival_unit:
                    isad = self.make_isad_record(archival_unit, row)

                    try:
                        isad.save()
                        # print("Inserting %s" % archival_unit.title_full)
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

                if archival_unit:
                    isad = self.make_isad_record(archival_unit, row)

                    try:
                        isad.save()
                        # print("Inserting %s" % archival_unit.title_full)
                        self.add_isad_languages(isad)

                    except IntegrityError as e:
                        print('Error with %s: %s' % (archival_unit.title_full.encode('utf-8'), e.args[1]))

    def make_isad_record(self, archival_unit, row):
        sql_isad2 = "SELECT * FROM isad2 WHERE isad2.Id = %s"
        language2nd = False

        cursor = self.cnx.cursor(dictionary=True, buffered=True)
        cursor.execute(sql_isad2, (row['Id'],))

        isad2 = cursor.fetchone()

        tz_budapest = timezone('Europe/Budapest')

        updated_by = get_user(row['Last edited by']).username
        last_edited = tz_budapest.localize(row['Last edited']) if row['Last edited'] else datetime.now(tz_budapest)

        isad = Isad.objects.get_or_create(
            archival_unit=archival_unit,
            year_from=row['YearFrom']
        )[0]

        if isad2 and isad2["Scope and content"]:
            language2nd = True

        access_rights = row['Conditions governing access']
        reproduction_rights = row['Conditions governing reproduction']

        isad.legacy_id = row['Id']
        isad.original_locale = None
        isad.title = row['ArchivalUnitName']
        isad.reference_code = archival_unit.reference_code
        isad.description_level = archival_unit.level
        isad.year_to = row['YearTo']
        isad.accruals = True if row['Accruals'] == 'Expected' else False
        isad.access_rights = AccessRight.objects.filter(statement='Unknown').first() if not access_rights else None
        isad.access_rights_legacy = access_rights
        isad.reproduction_rights = \
            ReproductionRight.objects.filter(statement='Third party rights are to be cleared.').first() \
            if not reproduction_rights else None
        isad.reproduction_rights_legacy = reproduction_rights
        isad.date_predominant = row['Date(s)']
        isad.carrier_estimated = row['Extent and medium']
        isad.archival_history = row['Archival history']
        isad.scope_and_content_abstract = row['Scope and content']
        isad.appraisal = row['Appraisal, destruction and scheduling information']
        isad.system_of_arrangement_information = row['System of arrangement']
        isad.physical_characteristics = row['Physical characteristics and technical requirements']
        isad.publication_note = row['Publication note']
        isad.note = row['Note']
        isad.internal_note = row['Internal notes']
        isad.archivists_note = row["Archivist's Note"]
        isad.published = True if row['DatePublic'] else False
        isad.user_published = updated_by
        isad.date_published = last_edited
        isad.user_created = User.objects.get(username='finding.aids').username
        isad.date_created = last_edited
        isad.user_updated = updated_by
        isad.date_updated = last_edited

        if language2nd:
            isad.original_locale = Locale.objects.get(pk='HU')
            isad.carrier_estimated_original = isad2['Extent and medium']
            isad.archival_history_original = isad2['Archival history']
            isad.scope_and_content_abstract_original = isad2['Scope and content']
            isad.access_rights_legacy_original = isad2['Conditions governing access']
            isad.reproduction_rights_legacy = isad2['Conditions governing reproduction']
            isad.appraisal_original = isad2['Appraisal, destruction and scheduling information']
            isad.system_of_arrangement_information_original = isad2['System of arrangement']
            isad.physical_characteristics_original = isad2['Physical characteristics and technical requirements']
            isad.publication_note_original = isad2['Publication note']
            isad.note_original = isad2['Note']
            isad.internal_note_original = isad2['Internal notes']
            isad.archivists_note_original = isad2["Archivist's Note"]

        return isad

    def add_isad_languages(self, isad):
        sql_language = "SELECT languagesinisad.IsadId, Languages.* FROM Languages " \
                       "INNER JOIN languagesinisad ON languagesinisad.LanguageId = Languages.ID " \
                       "WHERE languagesinisad.IsadId = %s AND iso_code IS NOT NULL"

        cursor = self.cnx.cursor(dictionary=True, buffered=True)
        cursor.execute(sql_language, (isad.legacy_id,))

        for row in cursor:
            language = Language.objects.filter(Q(iso_639_2=row['iso_code']) | Q(iso_639_3=row['iso_code'])).first()
            if language:
                isad.language.add(language)
            else:
                print("I can't find equivalent for the language: %s" % row['Language'])
        isad.save()
