from __future__ import unicode_literals

from django.db import models
from archival_unit.models import ArchivalUnit


class Container(models.Model):
    id = models.AutoField(primary_key=True)

    archival_unit = models.ForeignKey('archival_unit.ArchivalUnit')
    primary_type = models.ForeignKey('controlled_list.PrimaryType')
    carrier_type = models.ForeignKey('controlled_list.CarrierType')

    container_no = models.IntegerField(default=1)
    container_label = models.CharField(max_length=255, blank=True, null=True)

    permanent_id = models.CharField(max_length=50, blank=True, null=True)
    legacy_id = models.CharField(max_length=50, blank=True, null=True)
    old_id = models.IntegerField(blank=True, null=True)

    user_created = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(blank=True, auto_now_add=True)

    user_updated = models.CharField(max_length=100, blank=True)
    date_updated = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'containers'
        unique_together = ('archival_unit', 'container_no')

    def __unicode__(self):
        return "Container #%s / %s" % (self.container_no, self.carrier_type)

