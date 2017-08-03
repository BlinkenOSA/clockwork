from __future__ import unicode_literals

import uuid as uuid

from django.db import models


from validators import validate_level, validate_status


class ArchivalUnit(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    accession = models.ManyToManyField('accession.Accession', blank=True)

    fonds = models.IntegerField()
    subfonds = models.IntegerField(default=0)
    series = models.IntegerField(default=0)

    sort = models.CharField(max_length=12, blank=True)

    title = models.CharField(max_length=500)
    title_full = models.CharField(max_length=2000, blank=True, null=True)
    acronym = models.CharField(max_length=50, blank=True, null=True)
    reference_code = models.CharField(max_length=20)
    reference_code_id = models.CharField(max_length=20)

    level = models.CharField(max_length=2, validators=[validate_level])
    status = models.CharField(max_length=10, default='Final', validators=[validate_status])
    ready_to_publish = models.BooleanField(default=False)

    user_created = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(blank=True, auto_now_add=True)

    user_updated = models.CharField(max_length=100, blank=True)
    date_updated = models.DateTimeField(blank=True, null=True, auto_now=True)

    def save(self, **kwargs):
        self.sort = '%04d%04d%04d' % (self.fonds, self.subfonds, self.series)

        if self.level == 'F':
            self.reference_code = 'HU OSA ' + str(self.fonds)
            self.reference_code_id = 'hu_osa_' + str(self.fonds)
            self.title_full = self.reference_code + ' ' + self.title

        elif self.level == 'SF':
            self.reference_code = 'HU OSA ' + str(self.fonds) + '-' + str(self.subfonds)
            self.reference_code_id = 'hu_osa_' + str(self.fonds) + '-' + str(self.subfonds)
            fonds_title = self.parent.title
            self.title_full = self.reference_code + ' ' + fonds_title + ': ' + self.title

        else:
            self.reference_code = 'HU OSA ' + str(self.fonds) + '-' + str(self.subfonds) + '-' + str(self.series)
            self.reference_code_id = 'hu_osa_' + str(self.fonds) + '-' + str(self.subfonds) + '-' + str(self.series)
            subfonds_title = self.parent.title
            fonds_title = self.parent.parent.title
            self.title_full = self.reference_code + ' ' + fonds_title + ': ' + subfonds_title + ': ' + self.title

        super(ArchivalUnit, self).save()

    def __unicode__(self):
        return ' '.join((self.reference_code, self.title))

    class Meta:
        db_table = 'archival_units'
        ordering = ['fonds', 'subfonds', 'series']
        unique_together = (("fonds", "subfonds", "series", "level"),)
