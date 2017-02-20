from __future__ import unicode_literals

from django.db import models


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    alpha2 = models.CharField(max_length=2, blank=True, null=True)
    alpha3 = models.CharField(max_length=3)
    authority_url = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(unique=True, max_length=100)

    def __unicode__(self):
        return self.country

    class Meta:
        db_table = 'authority_countries'
        ordering = ['country']


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    alpha2 = models.CharField(max_length=10, blank=True, null=True)
    alpha3 = models.CharField(max_length=10)
    authority_url = models.CharField(max_length=200, blank=True, null=True)
    language = models.CharField(unique=True, max_length=100)

    def __unicode__(self):
        return self.language

    class Meta:
        db_table = 'authority_languages'
        ordering = ['language']
