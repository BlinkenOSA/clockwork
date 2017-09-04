from __future__ import unicode_literals

import uuid as uuid
from django.db import models
from django_date_extensions.fields import ApproximateDateField

from controlled_list.models import PrimaryType, PersonRole, CorporationRole, GeoRole, LanguageUsage
from authority.models import Person, Place, Corporation, Country, Language


class FindingAidsEntity(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    container = models.ForeignKey('container.Container', on_delete=models.PROTECT)
    original_locale = models.ForeignKey('controlled_list.Locale', blank=True, null=True, on_delete=models.PROTECT)
    legacy_id = models.CharField(max_length=200, blank=True, null=True)
    archival_reference_code = models.CharField(max_length=50, blank=True, null=True)

    FINDING_AIDS_LEVEL = [('F', 'Folder'), ('I', 'Item')]
    level = models.CharField(max_length=1, choices=FINDING_AIDS_LEVEL, default='F')

    # Required fields
    folder_no = models.IntegerField(default=0)
    sequence_no = models.IntegerField(default=0, blank=True, null=True)

    title = models.CharField(max_length=300)
    title_given = models.BooleanField(default=False)
    title_original = models.CharField(max_length=300, blank=True)

    date_from = ApproximateDateField()
    date_to = ApproximateDateField(blank=True)
    date_ca_span = models.IntegerField(blank=True, default=0)

    contents_summary = models.TextField(blank=True, null=True)
    contents_summary_original = models.TextField(blank=True, null=True)

    # Optional fields
    administrative_history = models.TextField(blank=True, null=True)
    administrative_history_original = models.TextField(blank=True, null=True)

    primary_type = models.ForeignKey('controlled_list.PrimaryType', default=1, on_delete=models.PROTECT)
    genre = models.ManyToManyField('authority.Genre', blank=True, null=True)

    # Associated Fields
    spatial_coverage_country = models.ManyToManyField('authority.Country', blank=True, related_name='spatial_coverage_countries')
    spatial_coverage_place = models.ManyToManyField('authority.Place', blank=True, related_name='spatial_coverage_places')

    # Subject Fields
    subject_person = models.ManyToManyField('authority.Person', blank=True, related_name='subject_poeple')
    subject_corporation = models.ManyToManyField('authority.Corporation', blank=True, related_name='subject_corporations')
    subject_heading = models.ManyToManyField('authority.Subject', blank=True)
    subject_keyword = models.ManyToManyField('controlled_list.Keyword', blank=True)

    # Extra metadata fields
    language_statement = models.CharField(max_length=300, blank=True, null=True)
    language_statement_original = models.CharField(max_length=300, blank=True, null=True)

    physical_description = models.CharField(max_length=300, blank=True, null=True)
    physical_description_original = models.CharField(max_length=300, blank=True, null=True)

    physical_condition = models.CharField(max_length=200, blank=True, null=True)

    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    duration = models.TimeField(blank=True, null=True)

    dimensions = models.TextField(max_length=200, blank=True, null=True)

    # Notes
    note = models.CharField(max_length=300, blank=True, null=True)
    note_original = models.CharField(max_length=300, blank=True, null=True)
    internal_note = models.CharField(max_length=300, blank=True, null=True)

    user_created = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(blank=True, auto_now_add=True)

    user_updated = models.CharField(max_length=100, blank=True)
    date_updated = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'fa_entities'

    def save(self, **kwargs):
        if self.level == 'F':
            self.archival_reference_code = "%s/%s:%s" % (self.container.archival_unit.reference_code,
                                                         self.container.container_no,
                                                         self.folder_no)
        else:
            self.archival_reference_code = "%s/%s:%s-%s" % (self.container.archival_unit.reference_code,
                                                            self.container.container_no,
                                                            self.folder_no,
                                                            self.sequence_no)

        super(FindingAidsEntity, self).save()


class FindingAidsEntityAlternativeTitle(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', on_delete=models.CASCADE)

    alternative_title = models.CharField(max_length=300)
    title_given = models.BooleanField(default=False)

    class Meta:
        db_table = 'finding_aids_alternative_titles'


class FindingAidsEntityCreator(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', on_delete=models.CASCADE)
    creator = models.CharField(max_length=300)
    CREATOR_ROLE = [('COL', 'Collector'), ('CRE', 'Creator')]
    role = models.CharField(max_length=3, choices=CREATOR_ROLE, default='CRE')

    class Meta:
        db_table = 'finding_aids_creators'


class FindingAidsEntityPlaceOfCreation(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', on_delete=models.CASCADE)
    place = models.CharField(max_length=200)

    class Meta:
        db_table = 'finding_aids_places_of_creation'


class FindingAidsEntitySubject(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)

    class Meta:
        db_table = 'finding_aids_subjects'


class FindingAidsEntityAssociatedPerson(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', on_delete=models.CASCADE)
    associated_person = models.ForeignKey('authority.Person', on_delete=models.PROTECT)
    role = models.ForeignKey('controlled_list.PersonRole', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'finding_aids_associated_people'


class FindingAidsEntityAssociatedCorporation(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', on_delete=models.CASCADE)
    associated_corporation = models.ForeignKey('authority.Corporation', on_delete=models.PROTECT)
    role = models.ForeignKey('controlled_list.CorporationRole', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'finding_aids_associated_corporations'


class FindingAidsEntityAssociatedCountry(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', on_delete=models.CASCADE)
    associated_country = models.ForeignKey('authority.Country', on_delete=models.PROTECT)
    role = models.ForeignKey('controlled_list.GeoRole', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'finding_aids_associated_countries'


class FindingAidsEntityAssociatedPlace(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', on_delete=models.CASCADE)
    associated_place = models.ForeignKey('authority.Place', on_delete=models.PROTECT)
    role = models.ForeignKey('controlled_list.GeoRole', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'finding_aids_associated_places'


class FindingAidsEntityLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', on_delete=models.CASCADE)
    language = models.ForeignKey('authority.Language', on_delete=models.PROTECT)
    role = models.ForeignKey('controlled_list.LanguageUsage', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'finding_aids_languages'


class FindingAidsEntityExtent(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', on_delete=models.CASCADE)
    extent_number = models.IntegerField(blank=True, null=True)
    extent_unit = models.ForeignKey('controlled_list.ExtentUnit', on_delete=models.CASCADE)

    class Meta:
        db_table = 'finding_aids_extents'
