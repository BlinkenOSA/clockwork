from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget
from authority.models import *


class CountrySelect2Widget(ModelSelect2Widget):
    model = Country
    search_fields = [
        'country__icontains',
    ]


class CountrySelect2MultipleWidget(ModelSelect2MultipleWidget):
    model = Country
    search_fields = [
        'country__icontains',
    ]


class LanguageSelect2MultipleWidget(ModelSelect2MultipleWidget):
    model = Language
    search_fields = [
        'language__icontains',
    ]


class GenreSelect2MultipleWidget(ModelSelect2MultipleWidget):
    model = Genre
    search_fields = [
        'genre__icontains',
    ]


class CorporationSelect2Widget(ModelSelect2Widget):
    model = Corporation
    search_fields = [
        'name__icontains'
    ]


class CorporationSelect2MultipleWidget(ModelSelect2MultipleWidget):
    model = Corporation
    search_fields = [
        'country__icontains',
    ]


class PersonSelect2Widget(ModelSelect2Widget):
    model = Person
    search_fields = [
        'first_name__icontains', 'last_name__icontains',
    ]


class PersonSelect2MultipleWidget(ModelSelect2MultipleWidget):
    model = Person
    search_fields = [
        'first_name__icontains', 'last_name__icontains',
    ]


class PlaceSelect2Widget(ModelSelect2Widget):
    model = Place
    search_fields = [
        'place__icontains'
    ]


class PlaceSelect2MultipleWidget(ModelSelect2MultipleWidget):
    model = Place
    search_fields = [
        'place__icontains'
    ]
