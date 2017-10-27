import mysql.connector
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import IntegrityError
from userena.models import UserenaSignup
from django.conf import settings


class Command(BaseCommand):
    help = 'Migrate users from the migradion DB.'

    def handle(self, *args, **options):
        if settings.MIGRATION_DB:
            cnx = mysql.connector.connect(user=settings.MIGRATION_DB['USER'],
                                          password=settings.MIGRATION_DB['PASSWORD'],
                                          host=settings.MIGRATION_DB['HOST'],
                                          database='clkwrk_import_users')
            cursor = cnx.cursor(dictionary=True, buffered=True)

            query = ("SELECT * FROM users")
            cursor.execute(query)

            for row in cursor:
                try:
                    user = User.objects.create_user(username=row['username'],
                                                    email=row['email'],
                                                    password=row['username']+'1209')
                    user.first_name = row['first_name']
                    user.last_name = row['last_name']
                    user.save()
                    usu = UserenaSignup(user=user)
                except IntegrityError:
                    print ("User %s already exists!" % row['username'])

            cnx.close()
        else:
            print ("Missing 'migration' database setting in 'settings.py'")
