from datetime import datetime
import mysql.connector
from django.core.management import BaseCommand
from django.conf import settings
from django.db import IntegrityError
from pytz import timezone

from archival_unit.models import ArchivalUnit
from container.models import Container
from controlled_list.models import PrimaryType, CarrierType
from migration.management.commands.common_functions import get_user


class Command(BaseCommand):
    help = 'Migrate Containers.'

    def handle(self, *args, **options):
        if settings.MIGRATION_DB:
            cnx = mysql.connector.connect(user=settings.MIGRATION_DB['USER'],
                                          password=settings.MIGRATION_DB['PASSWORD'],
                                          host=settings.MIGRATION_DB['HOST'],
                                          database=settings.MIGRATION_DB['DB'])

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
                  "INNER JOIN Container ON Main.ContType = Container.ID " \
                  "WHERE Main.ListNo = 1 AND Main.FondsID >= 0 " \
                  "ORDER BY FondsID, SubfondsID, SeriesID, ListNo, Container"

            cursor.execute(sql)

            pt1 = {
                1: PrimaryType.objects.get(type='Text'),
                3: PrimaryType.objects.get(type='Electronic Record'),
                4: PrimaryType.objects.get(type='Still Image')
            }

            pt2 = {
                'V': PrimaryType.objects.get(type='Video'),
                'SI': PrimaryType.objects.get(type='Still Image'),
                'A': PrimaryType.objects.get(type='Audio'),
                'TXT': PrimaryType.objects.get(type='Text')
            }

            carrier_map = {
                'Archival boxes': CarrierType.objects.get(type='Archival box'),
                'Archival card boxes': CarrierType.objects.get(type='Archival card box'),
                'Boxes of color prints': CarrierType.objects.get(type='Boxes of color prints'),
                'Audio cassette': CarrierType.objects.get(type='Audio cassette'),
                'Beta SP': CarrierType.objects.get(type='Beta SP'),
                'VHS': CarrierType.objects.get(type='VHS'),
                'CD-ROM': CarrierType.objects.get(type='CD-ROM'),
                'Rolls of 35mm microfilm in microfilm cabinet':
                    CarrierType.objects.get(type='Rolls of 35 mm microfilm in microfilm cabinet'),
                'Rolls of 16mm microfilm in microfilm cabinet':
                    CarrierType.objects.get(type='Rolls of 16 mm microfilm in microfilm cabinet'),
                'SVHS': CarrierType.objects.get(type='SVHS'),
                'Plastic card box': CarrierType.objects.get(type='VHS'),
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

                if row['Medium'] != 2:
                    pt = pt1[row['Medium']]
                else:
                    if row['Type']:
                        pt = pt2[row['Type']]
                    else:
                        pt = PrimaryType.objects.get(type='Video')

                created_by = get_user(row['UserCreated']).username
                created = tz_budapest.localize(row['DateCreated']) if row['DateCreated'] \
                    else datetime.now(tz_budapest)

                last_edited_by = get_user(row['UserChanged']).username
                last_edited = tz_budapest.localize(row['DateChanged']) if row['DateChanged'] \
                    else datetime.now(tz_budapest)

                container = Container(
                    archival_unit=archival_unit,
                    primary_type=pt,
                    carrier_type=carrier_map[row['Description']],
                    container_no=int(row['Container']),
                    container_label=row['Notes'],
                    legacy_id=row['InternalNotes'],
                    old_id=row['ID'],
                    user_created=created_by,
                    date_created=created,
                    user_updated=last_edited_by,
                    date_updated=last_edited
                )

                try:
                    container.save()
                    print("Inserting %s-%s" % (container.archival_unit.reference_code, container.container_no))
                except IntegrityError as e:
                    print('Error with %s-%s: %s' % (container.archival_unit.reference_code,
                                                     container.container_no,
                                                     e.args[1]))
                except Exception as e:
                    print('Some error - %s - Skipping' % e)

            cnx.close()
        else:
            print("Missing 'migration' database setting in 'settings.py'")


