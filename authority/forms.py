from django.forms import ModelForm
from extra_views import InlineFormSet

from authority.models import Country, Corporation, Person, Language, Place, Subject, Genre, PersonOtherFormat, \
    CorporationOtherFormat


class CountryForm(ModelForm):
    class Meta:
        model = Country
        fields = '__all__'
        labels = {
            'authority_url': 'Authority URL',
            'wiki_url': 'Wikipedia URL'
        }


class LanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = '__all__'
        labels = {
            'authority_url': 'Authority URL',
            'wiki_url': 'Wikipedia URL'
        }


class CorporationForm(ModelForm):
    class Meta:
        model = Corporation
        fields = '__all__'
        labels = {
            'authority_url': 'Authority URL',
            'wiki_url': 'Wikipedia URL',
            'other_url': 'Other URL'
        }


class CorporationOtherNamesInLine(InlineFormSet):
    extra = 1
    model = CorporationOtherFormat
    fields = '__all__'
    can_delete = True
    prefix = 'corporation_other_names'


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        labels = {
            'authority_url': 'Authority URL',
            'wiki_url': 'Wikipedia URL',
            'other_url': 'Other URL'
        }


class PersonOtherNamesInLine(InlineFormSet):
    extra = 1
    model = PersonOtherFormat
    fields = '__all__'
    can_delete = True
    prefix = 'people_other_names'


class PlaceForm(ModelForm):
    class Meta:
        model = Place
        fields = '__all__'
        labels = {
            'authority_url': 'Authority URL',
            'wiki_url': 'Wikipedia URL'
        }


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'
        labels = {
            'authority_url': 'Authority URL',
            'wiki_url': 'Wikipedia URL',
            'other_url': 'Other URL'
        }


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        labels = {
            'authority_url': 'Authority URL',
            'wiki_url': 'Wikipedia URL',
            'other_url': 'Other URL'
        }