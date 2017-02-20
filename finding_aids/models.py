from __future__ import unicode_literals

from django.db import models
from django_date_extensions.fields import ApproximateDateField


class FindingAidsEntity(models.Model):
    id = models.AutoField(primary_key=True)
    container = models.ForeignKey('container.Container')
    original_locale = models.ForeignKey('controlled_list.Locale', blank=True, null=True)

    # Required fields
    entity_no = models.IntegerField(default=1)

    title = models.CharField(max_length=300)
    title_given = models.BooleanField(default=False)
    title_original = models.CharField(max_length=300)

    contents_summary = models.TextField(blank=True, null=True)
    contents_summary_original = models.TextField(blank=True, null=True)

    date_from = ApproximateDateField(blank=True, null=True)
    date_to = ApproximateDateField(blank=True, null=True)

    user_created = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(blank=True, auto_now_add=True)

    user_updated = models.CharField(max_length=100, blank=True)
    date_updated = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'fa_entities'
