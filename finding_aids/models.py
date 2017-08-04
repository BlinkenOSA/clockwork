from __future__ import unicode_literals

import uuid as uuid
from django.db import models
from django_date_extensions.fields import ApproximateDateField

from controlled_list.models import PrimaryType, PersonRoles, CorporationRoles, GeoRoles, LanguageUsage
from authority.models import Person, Place, Corporation, Country, Language


class FindingAidsEntity(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    container = models.ForeignKey('container.Container')
    original_locale = models.ForeignKey('controlled_list.Locale', blank=True, null=True)

    FINDING_AIDS_LEVEL = [('F', 'Folder'), ('I', 'Item')]
    level = models.CharField(max_length=1, choices=FINDING_AIDS_LEVEL, default='F')

    # Required fields
    folder_no = models.IntegerField(default=0)
    item_no = models.IntegerField(default=0)

    title = models.CharField(max_length=300)
    title_given = models.BooleanField(default=False)
    title_original = models.CharField(max_length=300, blank=True)

    date_from = ApproximateDateField()
    date_to = ApproximateDateField(blank=True)
    date_ca_span = models.IntegerField(blank=True, default=0)

    # Optional fields
    administrative_history = models.TextField(blank=True, null=True)
    administrative_history_original = models.TextField(blank=True, null=True)

    primary_type = models.ForeignKey('controlled_list.PrimaryType', default=1)
    genre = models.ManyToManyField('authority.Genre')
    language_statement = models.CharField(max_length=300, blank=True, null=True)

    contents_summary = models.TextField(blank=True, null=True)
    contents_summary_original = models.TextField(blank=True, null=True)

    spatial_coverage_country = models.ManyToManyField('authority.Country', related_name='spatial_coverage_countries')
    spatial_coverage_place = models.ManyToManyField('authority.Place', related_name='spatial_coverage_places')

    subject_person = models.ManyToManyField('authority.Person', related_name='subject_poeple')
    subject_corporation = models.ManyToManyField('authority.Corporation', related_name='subject_corporations')
    subject_heading = models.ManyToManyField('authority.Subject')
    subject_keyword = models.ManyToManyField('controlled_list.Keyword')

    note = models.CharField(max_length=300, blank=True, null=True)
    internal_note = models.CharField(max_length=300, blank=True, null=True)

    user_created = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(blank=True, auto_now_add=True)

    user_updated = models.CharField(max_length=100, blank=True)
    date_updated = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'fa_entities'


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
    associated_person = models.ForeignKey('authority.Person', on_delete=models.CASCADE)
    role = models.ForeignKey('controlled_list.PersonRoles', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'finding_aids_associated_people'


class FindingAidsEntityAssociatedCorporation(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', on_delete=models.CASCADE)
    associated_corporation = models.ForeignKey('authority.Corporation', on_delete=models.CASCADE)
    role = models.ForeignKey('controlled_list.CorporationRoles', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'finding_aids_associated_corporations'


class FindingAidsEntityAssociatedCountry(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', on_delete=models.CASCADE)
    associated_country = models.ForeignKey('authority.Country', on_delete=models.CASCADE)
    role = models.ForeignKey('controlled_list.GeoRoles', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'finding_aids_associated_countries'


class FindingAidsEntityAssociatedPlace(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', on_delete=models.CASCADE)
    associated_country = models.ForeignKey('authority.Place', on_delete=models.CASCADE)
    role = models.ForeignKey('controlled_list.GeoRoles', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'finding_aids_associated_places'


class FindingAidsLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', on_delete=models.CASCADE)
    language = models.ForeignKey('authority.Language', on_delete=models.CASCADE)
    role = models.ForeignKey('controlled_list.LanguageUsage', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'finding_aids_languages'
