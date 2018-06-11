# coding: utf-8
import mysql.connector
from datetime import datetime
from django.core.management import BaseCommand
from django.conf import settings
from django.db import IntegrityError
from pytz import timezone

from isaar.models import Isaar, IsaarStandardizedName, IsaarOtherName, IsaarParallelName
from isad.models import Isad
from migration.management.commands.common_functions import get_user, get_approx_date, get_approx_date_from_string


class Command(BaseCommand):
    help = 'Migrate ISAAR Records.'

    def handle(self, *args, **options):
        if settings.MIGRATION_DB:
            cnx = mysql.connector.connect(user=settings.MIGRATION_DB['USER'],
                                          password=settings.MIGRATION_DB['PASSWORD'],
                                          host=settings.MIGRATION_DB['HOST'],
                                          database=settings.MIGRATION_DB['DB'])

            sql = "SELECT * FROM isaar ORDER BY FondsID, SubfondsID, SeriesID"

            cursor = cnx.cursor(dictionary=True, buffered=True)
            cursor.execute(sql)

            tz_budapest = timezone('Europe/Budapest')

            for row in cursor:
                created_by = get_user(row['Last edited by']).username
                updated_by = get_user(row['Last edited by']).username

                last_edited = self.get_last_edited(row['Last edited'])

                isaar, rec_created = Isaar.objects.get_or_create(
                    name=row['Authority Entry']
                )

                isaar.legacy_id = row['ID']
                isaar.type = row['Type of Archival Authority Record'][0]
                isaar.date_existence_from = get_approx_date_from_string(row['DateFrom'])
                isaar.date_existence_to = get_approx_date_from_string(row['DateTo'])
                isaar.function = row['Mandate, functions and sphere of activity']
                isaar.legal_status = row['Legal status']
                isaar.internal_structure = row['Administrative structure']
                isaar.internal_note = row["Archivist's Note"]
                isaar.history = row['Other significant information']
                isaar.user_created = created_by
                isaar.user_updated = updated_by
                isaar.status = 'Final' if row['CanGoPublic'] == 1 else 'Draft'

                try:
                    isaar.save()
                    # print("Inserting %s" % isaar.name)

                    if rec_created:
                        self.get_parallel_names(row['Parallel Entry/Entries'], isaar)
                        self.get_other_names(row['Non-preferred Term(s)'], isaar)

                    isaar.date_created = tz_budapest.localize(last_edited)
                    isaar.date_updated = tz_budapest.localize(last_edited)
                    isaar.save()

                    # Add ISAAR to ISAD(G)
                    ref_code = "HU OSA %s" % row['FondsID']
                    if row['SubfondsID']:
                        ref_code = "HU OSA %s-%s" % (row['FondsID'], row['SubfondsID'])
                    if row['SeriesID']:
                        ref_code = "HU OSA %s-%s-%s" % (row['FondsID'], row['SubfondsID'], row['SeriesID'])

                    isad = Isad.objects.filter(reference_code=ref_code).first()

                    if isad:
                        isad.isaar.add(isaar)
                        isad.save()

                except IntegrityError as e:
                    print('Error with %s: %s' % (isaar.name.encode('utf-8'), e.args[1]))

            cnx.close()
        else:
            print("Missing 'migration' database setting in 'settings.py'")

    def get_other_names(self, data, isaar):
        if data:
            entries = data.split(';')
            for entry in entries:
                isn = IsaarStandardizedName(
                    isaar=isaar,
                    name=entry.strip()
                )
                isn.save()

    def get_parallel_names(self, data, isaar):
        if data:
            entries = data.split(',')
            for entry in entries:
                ipn = IsaarParallelName(
                    isaar=isaar,
                    name=entry.strip()
                )
                ipn.save()

    def get_last_edited(self, last_edited):
        if last_edited:
            return datetime.strptime(last_edited, '%m/%d/%Y %I:%M:%S %p')
        else:
            return datetime.now()
