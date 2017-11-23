# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from archival_unit.models import ArchivalUnit
from container.models import Container


class MLREntity(models.Model):
    id = models.AutoField(primary_key=True)
    series = models.ForeignKey('archival_unit.ArchivalUnit')
    carrier_type = models.ForeignKey('controlled_list.CarrierType', on_delete=models.PROTECT)

    building = models.ForeignKey('controlled_list.Building', on_delete=models.PROTECT, blank=True, null=True)
    module = models.IntegerField(blank=True, null=True)
    row = models.IntegerField(blank=True, null=True)
    section = models.IntegerField(blank=True, null=True)
    shelf = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'mlr_records'
