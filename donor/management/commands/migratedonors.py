import mysql.connector
from django.core.management import BaseCommand
from django.conf import settings
from django.db import IntegrityError

from authority.models import Country
from donor.models import Donor


class Command(BaseCommand):
    help = 'Migrate Donors.'

    def handle(self, *args, **options):
        if settings.MIGRATION_DB:
            cnx = mysql.connector.connect(user=settings.MIGRATION_DB['USER'],
                                          password=settings.MIGRATION_DB['PASSWORD'],
                                          host=settings.MIGRATION_DB['HOST'],
                                          database='clkwrk_import_accession')

            sql = "SELECT donor.*, countries.Country FROM donor LEFT JOIN countries ON donor.CountryId = countries.ID"

            cursor = cnx.cursor(dictionary=True, buffered=True)
            cursor.execute(sql)

            for row in cursor:
                country = Country.objects.filter(country=row['Country']).first()

                if not country:
                    print ("Check country - %s" % row['Country'])
                else:
                    donor = Donor(
                        old_id=row['ID'],
                        name=row['DonorName'],
                        postal_code=row['PostalCode'] if row['PostalCode'] else 'N/A',
                        country=country,
                        city=row['City'].strip() if row['City'] else 'N/A',
                        address=row['Address'] if row['Address'] else 'N/A',
                        email=row['Email'].strip() if row['Email'] else 'N/A',
                        fax=row['Fax'],
                        phone=row['Telephone'],
                        website=row['Website'].strip() if row['Website'] else 'N/A',
                        note=row['Notes'],
                        user_created='finding.aids'
                    )

                    try:
                        donor.save()
                        print ("Inserting %s" % (row['DonorName']))
                    except IntegrityError as e:
                        print ('Error with %s: %s' % (row['DonorName'].encode('utf-8'), e.args[1]))

            cnx.close()
        else:
            print ("Missing 'migration' database setting in 'settings.py'")
