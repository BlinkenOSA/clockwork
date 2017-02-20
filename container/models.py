from __future__ import unicode_literals

from django.db import models


class Container(models.Model):
    id = models.AutoField(primary_key=True)

    archival_unit = models.ForeignKey('archival_unit.ArchivalUnit')
    primary_type = models.ForeignKey('controlled_list.PrimaryType')
    carrier_type = models.ForeignKey('controlled_list.CarrierType')

    container_no = models.IntegerField(default=1)
    container_label = models.CharField(max_length=255, blank=True, null=True)

    old_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'containers'
