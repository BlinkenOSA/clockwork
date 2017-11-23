# coding: utf-8
import calendar

import mysql.connector
from django.core.management import BaseCommand
from django.conf import settings
from django.db import IntegrityError
from pytz import timezone

from accession.models import Accession, AccessionMethod, AccessionCopyrightStatus, AccessionItem
from archival_unit.models import ArchivalUnit
from controlled_list.models import Building
from donor.models import Donor
from migration.management.commands.common_functions import get_user, get_approx_date


class Command(BaseCommand):
    help = 'Migrate Accession Records.'

    def handle(self, *args, **options):
        if settings.MIGRATION_DB:
            cnx = mysql.connector.connect(user=settings.MIGRATION_DB['USER'],
                                          password=settings.MIGRATION_DB['PASSWORD'],
                                          host=settings.MIGRATION_DB['HOST'],
                                          database='clkwrk_import_accession')

            sql_accession = "SELECT accession.* FROM accession ORDER BY Year, No, FondsID"

            cursor = cnx.cursor(dictionary=True, buffered=True)
            cursor.execute(sql_accession)

            tz_budapest = timezone('Europe/Budapest')

            for row in cursor:
                transfer_date = row['PreparedDate'] if row['PreparedDate'] else row['CreatedDate']
                created_date = row['CreatedDate'] if row['CreatedDate'] else row['PreparedDate']

                created_by = get_user(row['CreatedBy'])
                updated_by = get_user(row['ChangedBy'])
                method = self.get_accession_method(row['Method'])
                building = self.get_building(row['Building'])

                donor = Donor.objects.filter(old_id=row['DonorID']).first()

                creation_date_from = get_approx_date(row['Year1'], row['Month1'], row['Day1'])
                creation_date_to = get_approx_date(row['Year2'], row['Month2'], row['Day2'])

                copyright_status = self.get_copyright_status(row['Copyright'])

                if not donor:
                    print("Check donor - %s" % row['DonorID'])
                else:
                    accession = Accession(
                        seq='%d/%03d' % (row['Year'], row['No']),
                        title=row['FondsName'] if row['FondsName'] else 'Accession to Fonds %s' % row['FondsID'],
                        transfer_date=transfer_date,
                        description=row['Description'],
                        method=method,
                        building=building,
                        module=row['Module'],
                        row=row['Row'],
                        section=row['Section'],
                        shelf=row['Shelf'],
                        donor=donor,
                        creation_date_from=creation_date_from,
                        creation_date_to=creation_date_to,
                        copyright_status=copyright_status,
                        copyright_note=row['Copyright'],
                        note=row['Notes'],
                        user_created=created_by.username,
                        user_updated=updated_by.username
                    )

                    try:
                        accession.save()
                        print ("Inserting %s" % accession.seq)

                        archival_unit = ArchivalUnit.objects.filter(level='F', fonds=row['FondsID']).first()
                        if archival_unit:
                            archival_unit.accession.add(accession)
                            archival_unit.save()

                        accession_items = self.collect_accession_items(cnx, row)
                        for accession_item in accession_items:
                            item = AccessionItem(
                                accession=accession,
                                quantity=accession_item[0],
                                container=accession_item[1],
                                content=accession_item[2]
                            )
                            item.save()

                        accession.date_created = tz_budapest.localize(created_date)
                        accession.save()

                    except IntegrityError as e:
                        print ('Error with %s: %s' % (accession.seq, e.args[1]))

            cnx.close()
        else:
            print("Missing 'migration' database setting in 'settings.py'")

    def get_accession_method(self, method):
        method_map = {
            'Deposit': 'Deposit (Non OSF)',
            'Donation (Non-Soros)': 'Donation (non-OSF)',
            'Donation (Soros records)': 'Donation (OSF)',
            'Internal transfer, OSA': 'OSA creation',
            'OSA Capture (AV)': 'OSA capture',
            'OSA records': 'OSA creation',
            'Purchase': 'OSA purchase',
            'Unknown': 'Unknown'
        }
        if method:
            return AccessionMethod.objects.filter(method=method_map[method]).first()
        else:
            return AccessionMethod.objects.filter(method='Unknown').first()

    def get_building(self, building):
        building_map = {
            'arany janos': 'Arany Janos u. 32.',
            'L': 'Arany Janos u. 32.',
            'Oktober 6': 'Oktober 6. u.',
            'Oktober 6 Vault Room': 'Oktober 6. u.',
            'Arany J. u. 32.': 'Arany Janos u. 32.',
            'Arany Janos 32': 'Arany Janos u. 32.',
            'Arany Janos 32.': 'Arany Janos u. 32.',
            'Asrany Janos 32': 'Arany Janos u. 32.',
            'Arany János utca 32.': 'Arany Janos u. 32.',
            'Aranu Janos u.32': 'Arany Janos u. 32.',
            'Arany János u. 32.': 'Arany Janos u. 32.',
            'Arany János u.  32': 'Arany Janos u. 32.',
            'Arany J. u. 32': 'Arany Janos u. 32.',
            'Budapest V., Arany János utca 32.': 'Arany Janos u. 32.',
            'Kerepesi Storage': 'Kerepesi',
            'Oktober 6. Vault Room': 'Oktober 6. u.',
            'Arany Janos u. 32': 'Arany Janos u. 32.',
            'Arany János u. 32': 'Arany Janos u. 32.',
            'Arany János 32': 'Arany Janos u. 32.',
            'Arany Janos utca 32.': 'Arany Janos u. 32.'
        }
        if building:
            try:
                return Building.objects.filter(building=building_map[building.encode('utf-8')]).first()
            except KeyError:
                pass
        else:
            return None

    def get_copyright_status(self, copyright):
        copyright_map = {
            'n/a': 'Unknown',
            'Copyright held by donor': 'Copyright held by Donor',
            'Copyright held by creator (other than donor)': 'Copyright held by Creator',
            'Copyright held by the producer': 'Copyright held by Other',
            'Copyright held by the CEU-Regents': 'Copyright held by Other',
            'Copyright held by other (see notes)': 'Copyright held by Other',
            'Copyright held by the New York State Board of Rege': 'Copyright held by Other',
            'Open Society Institute': 'Copyright held by OSF',
            'Yugoslav Television': 'Copyright held by Creator',
            'Unknown': 'Unknown',
            'Copyright held by AJC': 'Copyright held by Other'
        }
        if copyright:
            if 'Copyright held by:' in copyright:
                return AccessionCopyrightStatus.objects.filter(status='Copyright held by Donor').first()
            else:
                return AccessionCopyrightStatus.objects.filter(status=copyright_map[copyright]).first()
        else:
            return AccessionCopyrightStatus.objects.filter(status='Unknown').first()

    def collect_accession_items(self, cnx, accession):
        items = []
        sql_accession_items = "SELECT * FROM accessioneditems " \
                              "WHERE FondsID = %s AND AccessionYear = %s AND AccessionNo = %s"

        cursor = cnx.cursor(dictionary=True, buffered=True)
        cursor.execute(sql_accession_items, (accession['FondsID'], accession['Year'], accession['No']))

        for row in cursor:
            items.append([row['Quantity'], row['ContTypeName'], row['Description']])
        return items
