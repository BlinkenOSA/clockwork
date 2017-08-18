from __future__ import unicode_literals

from django.db import models
from django_date_extensions.fields import ApproximateDateField

from archival_unit.models import ArchivalUnit


class Isad(models.Model):
    id = models.AutoField(primary_key=True)
    archival_unit = models.OneToOneField('archival_unit.ArchivalUnit')
    original_locale = models.ForeignKey('controlled_list.Locale', blank=True, null=True)

    # Required fields
    title = models.CharField(max_length=255)
    reference_code = models.CharField(max_length=30)

    DESCRIPTION_LEVEL = [('F', 'Fonds'), ('SF', 'Subfonds'), ('S', 'Series')]
    description_level = models.CharField(max_length=10, choices=DESCRIPTION_LEVEL)
    year_from = models.IntegerField()
    year_to = models.IntegerField(blank=True, null=True)
    isaar = models.ManyToManyField('isaar.Isaar', blank=True)
    language = models.ManyToManyField('authority.Language')
    accruals = models.BooleanField(default=False)
    access_rights = models.ForeignKey('controlled_list.AccessRight')
    reproduction_rights = models.ForeignKey('controlled_list.ReproductionRight')
    rights_restriction_reason = models.ForeignKey('controlled_list.RightsRestrictionReason')

    # Identity
    date_predominant = models.CharField(max_length=200, blank=True, null=True)

    # Context
    administrative_history = models.TextField(blank=True, null=True)
    administrative_history_original = models.TextField(blank=True, null=True)
    archival_history = models.TextField(blank=True, null=True)
    archival_history_original = models.TextField(blank=True, null=True)

    # Content
    scope_and_content_abstract = models.TextField(blank=True, null=True)
    scope_and_content_abstract_original = models.TextField(blank=True, null=True)
    scope_and_content_narrative = models.TextField(blank=True, null=True)
    scope_and_content_narrative_original = models.TextField(blank=True, null=True)
    appraisal = models.TextField(blank=True, null=True)
    appraisal_original = models.TextField(blank=True, null=True)
    system_of_arrangement_information = models.TextField(blank=True, null=True)
    system_of_arrangement_information_original = models.TextField(blank=True, null=True)

    # Access & Use
    embargo = ApproximateDateField(blank=True)
    physical_characteristics = models.TextField(blank=True, null=True)
    physical_characteristics_original = models.TextField(blank=True, null=True)

    # Allied Materials
    publication_note = models.TextField(blank=True, null=True)
    publication_note_original = models.TextField(blank=True, null=True)

    # Notes
    note = models.TextField(blank=True, null=True)
    note_original = models.TextField(blank=True, null=True)
    internal_note = models.TextField(blank=True, null=True)
    internal_note_original = models.TextField(blank=True, null=True)
    archivists_note = models.TextField(blank=True, null=True)
    archivists_note_original = models.TextField(blank=True, null=True)
    rules_conventions = models.TextField(blank=True, null=True)

    # Approved/Published
    approved = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    class Meta:
        db_table = 'isad_recrods'


class IsadCreator(models.Model):
    id = models.AutoField(primary_key=True)
    isad = models.ForeignKey('Isad', on_delete=models.CASCADE)
    creator = models.CharField(max_length=300)

    class Meta:
        db_table = 'isad_creators'


class IsadExtent(models.Model):
    id = models.AutoField(primary_key=True)
    isad = models.ForeignKey('Isad', on_delete=models.CASCADE)
    approx = models.BooleanField(default=False)  # This field type is a guess.
    extent_number = models.IntegerField()
    extent_unit = models.ForeignKey('controlled_list.ExtentUnit', on_delete=models.CASCADE)

    class Meta:
        db_table = 'isad_extents'
        unique_together = (('isad', 'extent_unit'),)


class IsadCarrier(models.Model):
    id = models.AutoField(primary_key=True)
    isad = models.ForeignKey('Isad', on_delete=models.CASCADE)
    carrier_number = models.IntegerField()
    carrier_type = models.ForeignKey('controlled_list.CarrierType', on_delete=models.CASCADE)

    class Meta:
        db_table = 'isad_carriers'
        unique_together = (('isad', 'carrier_type'),)


class IsadRelatedFindingAids(models.Model):
    id = models.AutoField(primary_key=True)
    isad = models.ForeignKey('Isad', models.CASCADE)
    info = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'isad_related_finding_aids'


class IsadLocationOfOriginals(models.Model):
    id = models.AutoField(primary_key=True)
    isad = models.ForeignKey('Isad', models.CASCADE)
    info = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'isad_location_of_originals'


class IsadLocationOfCopies(models.Model):
    id = models.AutoField(primary_key=True)
    isad = models.ForeignKey('Isad', models.CASCADE)
    info = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'isad_location_of_copies'