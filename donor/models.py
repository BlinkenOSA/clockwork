from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
import uuid

from django.utils.translation import ugettext


class Donor(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    old_id = models.IntegerField(blank=True, null=True)

    name = models.CharField(unique=True, max_length=200, blank=True, null=True)

    first_name = models.CharField(max_length=200, blank=True)
    middle_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    corporation_name = models.CharField(max_length=200, blank=True)

    extra_info = models.CharField(max_length=200, blank=True)

    postal_code = models.CharField(max_length=20)
    country = models.ForeignKey('authority.Country', models.PROTECT)
    city = models.CharField(max_length=40)
    address = models.CharField(max_length=300)

    email = models.CharField(max_length=100, blank=True)
    fax = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True)

    note = models.TextField(blank=True, null=True)

    user_created = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(blank=True, auto_now_add=True)

    user_updated = models.CharField(max_length=100, blank=True)
    date_updated = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __unicode__(self):
        return self.name

    def clean(self):
        if self.first_name:
            self.name = "%s %s %s" % (self.first_name, self.middle_name, self.last_name)
        elif self.corporation_name:
            self.name = self.corporation_name
        else:
            raise ValidationError({'first_name': ugettext("Name or Corporation Name is mandatory!")})

    def get_address(self):
        return "%s %s, %s, %s" % (self.postal_code, self.country, self.city, self.address)

    class Meta:
        db_table = 'donor_records'
