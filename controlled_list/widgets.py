from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
from controlled_list.models import *


class CorporationRoleSelect2Widget(ModelSelect2Widget):
    model = CorporationRole
    search_fields = [
        'role__icontains'
    ]


class GeoRoleSelect2Widget(ModelSelect2Widget):
    model = GeoRole
    search_fields = [
        'role__icontains'
    ]


class KeywordSelect2MultipleWidget(ModelSelect2MultipleWidget):
    model = Keyword
    search_fields = [
        'keyword__icontains'
    ]


class PersonRoleSelect2Widget(ModelSelect2Widget):
    model = PersonRole
    search_fields = [
        'role__icontains'
    ]


class LanguageUsageSelect2Widget(ModelSelect2Widget):
    model = LanguageUsage
    search_fields = [
        'usage__icontains'
    ]


class ExtentUnitSelect2Widget(ModelSelect2Widget):
    model = ExtentUnit
    search_fields = [
        'unit__icontains'
    ]