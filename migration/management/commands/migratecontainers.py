from datetime import datetime
import mysql.connector
from django.core.management import BaseCommand, CommandError
from django.conf import settings
from django.db import IntegrityError
from pytz import timezone

from archival_unit.models import ArchivalUnit
from container.models import Container
from controlled_list.models import PrimaryType, CarrierType
from migration.management.commands.common_functions import get_user


class Command(BaseCommand):
    help = 'Migrate Containers.'

    def add_arguments(self, parser):
        parser.add_argument('--fonds', dest='fonds', help='Fonds Number')
        parser.add_argument('--subfonds', dest='subfonds', help='Subfonds Number')
        parser.add_argument('--series', dest='series', help='Series Number')
        parser.add_argument('--container_list', dest='container_list', help='Container List')

    def handle(self, *args, **options):
        if settings.MIGRATION_DB:
            cnx = mysql.connector.connect(user=settings.MIGRATION_DB['USER'],
                                          password=settings.MIGRATION_DB['PASSWORD'],
                                          host=settings.MIGRATION_DB['HOST'],
                                          database=settings.MIGRATION_DB['DB'])
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

            cursor = cnx.cursor(dictionary=True, buffered=True)
            sql = "SELECT Main.ID, Main.FondsID, Main.SubfondsID, Main.SeriesID, Main.ListNo, ListsInSeries.Medium, " \
                  "AVContainerDecision.Type, Main.Container, Main.Notes, Main.InternalNotes, Main.DateCreated, " \
                  "Main.DateChanged, Main.UserCreated, Main.UserChanged, Container.Description " \
                  "FROM ListsInSeries " \
                  "LEFT JOIN AVContainerDecision ON ListsInSeries.FondsId = AVContainerDecision.F AND " \
                  "ListsInSeries.SubfondsId = AVContainerDecision.SF AND " \
                  "ListsInSeries.SeriesId = AVContainerDecision.S " \
                  "INNER JOIN Main ON Main.FondsID = ListsInSeries.FondsId AND " \
                  "Main.SubfondsID = ListsInSeries.SubfondsId AND " \
                  "Main.SeriesID = ListsInSeries.SeriesId AND " \
                  "Main.ListNo = ListsInSeries.ListNo " \
                  "INNER JOIN Container ON Main.ContType = Container.ID "

            sql = sql + "WHERE " + where + " ORDER BY FondsID, SubfondsID, SeriesID, ListNo, Container"

            cursor.execute(sql)

            carrier_map = {
                'Archival boxes': CarrierType.objects.get(type='Archival boxes'),
                'Archival card boxes': CarrierType.objects.get(type='Archival card box'),
                'Boxes of color prints': CarrierType.objects.get(type='Boxes of color prints'),
                'Audio cassette': CarrierType.objects.get(type='Audio cassette'),
                'Beta SP': CarrierType.objects.get(type='BetaSP PAL'),
                'VHS': CarrierType.objects.get(type='VHS PAL'),
                'CD-ROM': CarrierType.objects.get(type='CD-ROM'),
                'Rolls of 35mm microfilm in microfilm cabinet':
                    CarrierType.objects.get(type='Rolls of 35 mm microfilm in microfilm cabinet'),
                'Rolls of 16mm microfilm in microfilm cabinet':
                    CarrierType.objects.get(type='Rolls of 16 mm microfilm in microfilm cabinet'),
                'SVHS': CarrierType.objects.get(type='SVHS'),
                'Plastic card box': CarrierType.objects.get(type='Plastic card box'),
                "Floppy 3''": CarrierType.objects.get(type='Floppy 3.5'),
                "Floppy 5''": CarrierType.objects.get(type='Floppy 5.25'),
                'DVD-ROM': CarrierType.objects.get(type='DVD-ROM'),
                'SDLT I': CarrierType.objects.get(type='SDLT I'),
                'Oversized box (40cm)': CarrierType.objects.get(type='Oversized box (40 cm)'),
                'S-VHS C': CarrierType.objects.get(type='SVHS-C'),
                'mini CD-R': CarrierType.objects.get(type='mini CD-R'),
                'mini DV': CarrierType.objects.get(type='mini DV'),
                'Oversized folder': CarrierType.objects.get(type='Oversized folder'),
                'Digital - Text': CarrierType.objects.get(type='Digital container'),
                'Digital - Audio': CarrierType.objects.get(type='Digital container'),
                'Digital - Video': CarrierType.objects.get(type='Digital container'),
                'HDD': CarrierType.objects.get(type='HDD'),
                '[other]': CarrierType.objects.get(type='N/A'),
                'SDLT*': CarrierType.objects.get(type='SDLT I')
            }
            tz_budapest = timezone('Europe/Budapest')

            for row in cursor:
                archival_unit = ArchivalUnit.objects.filter(fonds=row['FondsID'],
                                                            subfonds=row['SubfondsID'],
                                                            series=row['SeriesID'],
                                                            level='S').first()

                created_by = get_user(row['UserCreated']).username
                created = tz_budapest.localize(row['DateCreated']) if row['DateCreated'] \
                    else datetime.now(tz_budapest)

                last_edited_by = get_user(row['UserChanged']).username
                last_edited = tz_budapest.localize(row['DateChanged']) if row['DateChanged'] \
                    else datetime.now(tz_budapest)

                container = Container.objects.filter(
                    archival_unit=archival_unit,
                    container_no=int(row['Container'])
                ).first()

                if not container:
                    print("Inserting %s-%s" % (archival_unit.reference_code, int(row['Container'])))
                    container = Container.objects.create(
                        archival_unit=archival_unit,
                        container_no=int(row['Container']),
                        carrier_type=carrier_map[row['Description']]
                    )
                else:
                    print("Updating %s-%s" % (container.archival_unit.reference_code, container.container_no))
                    container.carrier_type = carrier_map[row['Description']]

                container.container_label = row['Notes']
                container.legacy_id = row['InternalNotes']
                container.old_id = row['ID']
                container.user_created = created_by
                container.user_updated = last_edited_by
                container.date_created = created
                container.date_updated = last_edited

                container.save()

            cnx.close()
        else:
            print("Missing 'migration' database setting in 'settings.py'")


