# coding: utf-8
import calendar
import mysql.connector
from django.contrib.auth.models import User

from clockwork import settings


def get_approx_date_from_string(date):
    if date:
        chunks = map(lambda x: int(x), date.split('-'))
        if len(chunks) == 3:
            return "%04d-%02d-%02d" % (chunks[0], chunks[1], chunks[2])
        elif len(chunks) == 2:
            return "%04d-%02d-%02d" % (chunks[0], chunks[1], 0)
        elif len(chunks) == 1:
            return "%04d-%02d-%02d" % (chunks[0], 0, 0)
        else:
            return None
    else:
        return None


def get_approx_date(year, month, day):
    if year:
        back = "%04d" % year

        if month:
            month = list(calendar.month_name).index(month)
            back += "-%02d" % month
        else:
            back += "-00"

        if day:
            back += "-%02d" % day
        else:
            back += "-00"
        return back
    else:
        return None


def get_user(old_user):
    old_user = old_user.lower().strip() if old_user else None
    if old_user:
        cnx = mysql.connector.connect(user=settings.MIGRATION_DB['USER'],
                                      password=settings.MIGRATION_DB['PASSWORD'],
                                      host=settings.MIGRATION_DB['HOST'],
                                      database='clkwrk_import_users')
        cursor = cnx.cursor(buffered=True, dictionary=True)
        SQL = 'SELECT * FROM users WHERE olduser = %s'
        cursor.execute(SQL, (old_user,))

        if cursor.rowcount:
            rec = cursor.fetchone()
            return User.objects.filter(username=rec['username']).first()
        else:
            return User.objects.filter(username='finding.aids').first()
    else:
        return User.objects.filter(username='finding.aids').first()
