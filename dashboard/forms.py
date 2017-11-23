from django.forms import Form, ModelChoiceField
from django_select2.forms import ModelSelect2Widget

from archival_unit.models import ArchivalUnit


class DashboardArchivalUnitSelectForm(Form):
    fonds= ModelChoiceField(
        queryset=ArchivalUnit.objects.all(),
        required=False,
        widget=ModelSelect2Widget(
            queryset=ArchivalUnit.objects.filter(level='F').order_by('fonds', 'subfonds', 'series'),
            search_fields=['title__icontains', 'reference_code__icontains']
        )
    )
    subfonds = ModelChoiceField(
        queryset=ArchivalUnit.objects.all(),
        required=False,
        widget=ModelSelect2Widget(
            queryset=ArchivalUnit.objects.filter(level='SF').order_by('fonds', 'subfonds', 'series'),
            search_fields=['title__icontains', 'reference_code__icontains'],
            dependent_fields={'fonds': 'parent'}
        )
    )
    series = ModelChoiceField(
        queryset=ArchivalUnit.objects.all(),
        required=False,
        widget=ModelSelect2Widget(
            queryset=ArchivalUnit.objects.filter(level='S').order_by('fonds', 'subfonds', 'series'),
            search_fields=['title__icontains', 'reference_code__icontains'],
            dependent_fields={'subfonds': 'parent'}
        )
    )
