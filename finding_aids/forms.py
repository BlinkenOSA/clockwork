from django.forms import ModelChoiceField, Form, CharField

from archival_unit.models import ArchivalUnit
from archival_unit.widgets import ArchivalUnitSelect2Widget
from django_date_extensions.fields import ApproximateDateFormField

from controlled_list.models import Locale


class FindingAidsArchivalUnitForm(Form):
    archival_unit = ModelChoiceField(
        queryset=ArchivalUnit.objects.filter(level='S').order_by('fonds', 'subfonds', 'series'),
        widget=ArchivalUnitSelect2Widget()
    )


class FindingAidsInContainerForm(Form):
    title = CharField(max_length=300, required=True)
    title_original = CharField(max_length=300)

    date_from = ApproximateDateFormField(required=True)
    date_to = ApproximateDateFormField(required=False)

    original_locale = ModelChoiceField(queryset=Locale.objects.all())