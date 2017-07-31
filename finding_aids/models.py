from __future__ import unicode_literals

from django.db import models
from django_date_extensions.fields import ApproximateDateField

from controlled_list.models import PrimaryType


class FindingAidsEntity(models.Model):
    id = models.AutoField(primary_key=True)
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

    date_from = ApproximateDateField(blank=True)
    date_to = ApproximateDateField(blank=True)
    date_ca_span = models.IntegerField(default=0)

    # Optional fields
    administrative_history = models.TextField(blank=True, null=True)
    administrative_history_original = models.TextField(blank=True, null=True)

    associated_country = models.ManyToManyField('authority.Country', related_name='associated_countries')
    associated_place = models.ManyToManyField('authority.Place', related_name='associated_places')
    associated_person = models.ManyToManyField('authority.Person', related_name='associated_people')
    associated_corporation = models.ManyToManyField('authority.Corporation', related_name='associated_corporations')

    primary_type = models.ForeignKey('controlled_list.PrimaryType', default=1)
    genre = models.ManyToManyField('authority.Genre')

    language = models.ManyToManyField('authority.Language')
    language_statement = models.CharField(max_length=300, blank=True, null=True)
    contents_summary = models.TextField(blank=True, null=True)
    contents_summary_original = models.TextField(blank=True, null=True)

    spatial_coverage_country = models.ManyToManyField('authority.Country', related_name='spatial_coverage_countries')
    spatial_coverage_place = models.ManyToManyField('authority.Place', related_name='spatial_coverage_places')

    subject_person = models.ManyToManyField('authority.Person', related_name='subject_poeple')
    subject_corporation = models.ManyToManyField('authority.Corporation', related_name='subject_corporations')
    subject_heading = models.ManyToManyField('authority.Subject')
    subject_keyword = models.ManyToManyField('controlled_list.Keyword')

    user_created = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(blank=True, auto_now_add=True)

    user_updated = models.CharField(max_length=100, blank=True)
    date_updated = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'fa_entities'


class FindingAidsEntityAlternativeTitle(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', models.PROTECT)

    alternative_title = models.CharField(max_length=300)
    title_given = models.BooleanField(default=False)


class FindingAidsEntityCreator(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', models.PROTECT)
    creator = models.CharField(max_length=300)
    CREATOR_ROLE = [('COL', 'Collector'), ('CRE', 'Creator')]
    role = models.CharField(max_length=3, choices=CREATOR_ROLE, default='CRE')


class FindingAidsEntityPlaceOfCreation(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', models.PROTECT)
    place = models.CharField(max_length=200)


class FindingAidsEntitySubject(models.Model):
    id = models.AutoField(primary_key=True)
    fa_entity = models.ForeignKey('FindingAidsEntity', models.PROTECT)
    subject = models.CharField(max_length=200)

