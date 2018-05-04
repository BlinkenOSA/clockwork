import mysql.connector
from django.core.management import BaseCommand
from django.conf import settings
from django.db import IntegrityError

from archival_unit.models import ArchivalUnit
from controlled_list.models import Locale, ArchivalUnitTheme


class Command(BaseCommand):
    help = 'Migrate ArchivalUnits.'

    def handle(self, *args, **options):
        if settings.MIGRATION_DB:
            cnx = mysql.connector.connect(user=settings.MIGRATION_DB['USER'],
                                          password=settings.MIGRATION_DB['PASSWORD'],
                                          host=settings.MIGRATION_DB['HOST'],
                                          database=settings.MIGRATION_DB['DB'])
            self.insert_fonds(cnx)
            self.insert_subfonds(cnx)
            self.insert_series(cnx)

            cnx.close()
        else:
            print("Missing 'migration' database setting in 'settings.py'")

    def insert_fonds(self, cnx):
        cursor = cnx.cursor(dictionary=True, buffered=True)
        sql = "SELECT * FROM fonds"

        cursor.execute(sql)

        for row in cursor:
            archival_unit = ArchivalUnit(
                fonds=row['ID'],
                subfonds=0,
                series=0,
                level='F',
                title=row['Name'],
                acronym=row['Acronym'],
                user_created='finding.aids'
            )

            if row['Name2']:
                archival_unit.title_original = row['Name2']
                archival_unit.original_locale = Locale.objects.get(pk='HU')

            try:
                archival_unit.save()

                if row['CommunismAndColdWar']:
                    archival_unit.theme.add(ArchivalUnitTheme.objects.filter(theme='Communism & Cold War').first())

                if row['HumanRights']:
                    archival_unit.theme.add(ArchivalUnitTheme.objects.filter(theme='Human Rights').first())

                if row['SorosInstitution']:
                    archival_unit.theme.add(ArchivalUnitTheme.objects.filter(theme='Civil Society').first())

                archival_unit.save()
                # print("Inserting %s" % (row['ID']))
            except IntegrityError:
                print("Fonds %s already exists!" % row['ID'])

    def insert_subfonds(self, cnx):
        cursor = cnx.cursor(dictionary=True, buffered=True)
        sql = "SELECT * FROM subfonds"

        cursor.execute(sql)

        for row in cursor:
            parent_record = ArchivalUnit.objects.filter(fonds=row['FondsID'],
                                                        level='F').first()
            archival_unit = ArchivalUnit(
                fonds=row['FondsID'],
                parent=parent_record,
                subfonds=row['ID'],
                series=0,
                level='SF',
                title=row['Name'],
                acronym=row['Acronym'],
                user_created='finding.aids'
            )

            if row['Name2']:
                archival_unit.title_original = row['Name2']
                archival_unit.original_locale = Locale.objects.get(pk='HU')

            try:
                archival_unit.save()

                for theme in parent_record.theme.all():
                    archival_unit.theme.add(theme)

                archival_unit.save()
                # print("Inserting %s-%s" % (row['FondsID'], row['ID']))
            except IntegrityError:
                print("Subfonds %s-%s already exists!" % (row['FondsID'], row['ID']))

    def insert_series(self, cnx):
        cursor = cnx.cursor(dictionary=True, buffered=True)
        sql = "SELECT * FROM series"

        cursor.execute(sql)

        for row in cursor:
            parent_record = ArchivalUnit.objects.filter(fonds=row['FondsID'],
                                                        subfonds=row['SubfondsID'],
                                                        level='SF').first()
            archival_unit = ArchivalUnit(
                fonds=row['FondsID'],
                parent=parent_record,
                subfonds=row['SubfondsID'],
                series=row['ID'],
                level='S',
                title=row['Name'],
                acronym=row['Acronym'],
                user_created='finding.aids'
            )

            if row['Name2']:
                archival_unit.title_original = row['Name2']
                archival_unit.original_locale = Locale.objects.get(pk='HU')

            try:
                archival_unit.save()

                for theme in parent_record.theme.all():
                    archival_unit.theme.add(theme)

                archival_unit.save()
                # print("Inserting %s-%s-%s" % (row['FondsID'], row['SubfondsID'], row['ID']))
            except IntegrityError:
                print("Series %s-%s-%s already exists!" % (row['FondsID'], row['SubfondsID'], row['ID']))
