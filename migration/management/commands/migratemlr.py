from datetime import datetime
import mysql.connector
from django.core.management import BaseCommand
from django.conf import settings
from django.db import IntegrityError
from pytz import timezone

from archival_unit.models import ArchivalUnit
from container.models import Container
from controlled_list.models import PrimaryType, CarrierType, Building
from migration.management.commands.common_functions import get_user
from mlr.models import MLREntity, MLREntityLocation


class Command(BaseCommand):
    help = 'Migrate MLR Records.'

    def handle(self, *args, **options):
        if settings.MIGRATION_DB:
            mlr_records = MLREntity.objects.all()

            cnx = mysql.connector.connect(user=settings.MIGRATION_DB['USER'],
                              password=settings.MIGRATION_DB['PASSWORD'],
                              host=settings.MIGRATION_DB['HOST'],
                              database=settings.MIGRATION_DB['DB'])

            MLREntityLocation.objects.all().delete()

            for mlr_record in mlr_records:
                fonds = mlr_record.series.fonds
                subfonds = mlr_record.series.subfonds
                series = mlr_record.series.series

                cursor = cnx.cursor(dictionary=True, buffered=True)
                sql = "SELECT FondsId, SubfondsId, SeriesId, ListNo, Module, Row, Section, Shelf, LocationNotes " \
                      "FROM ListsInSeries WHERE FondsId = %s AND SubfondsId = %s AND SeriesId = %s AND ListNo = 1"

                cursor.execute(sql, (fonds, subfonds, series))
                row = cursor.fetchone()

                if row:
                    mlr_record.notes = row.get('LocationNotes', "")
                    mlr_record.save()

                    MLREntityLocation.objects.create(
                        mlr=mlr_record,
                        building=Building.objects.get(id=1),
                        module=row['Module'],
                        row=row['Row'],
                        section=row['Section'],
                        shelf=row['Shelf']
                    )

