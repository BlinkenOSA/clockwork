from django_select2.forms import ModelSelect2Widget

from archival_unit.models import ArchivalUnit


class ArchivalUnitSelect2Widget(ModelSelect2Widget):
    model = ArchivalUnit
    search_fields = ['title__icontains', 'reference_code__icontains']
    attrs = {'placeholder': '-- Select Archival Unit --'}

    def label_from_instance(self, obj):
        return '<span class="archival_unit_title level_' + obj.level + '">' + obj.title_full + '</span>'


class ArchivalUnitSeriesSelect2Widget(ModelSelect2Widget):
    search_fields = ['title__icontains', 'reference_code__icontains']
    attrs = {'placeholder': '-- Select Archival Unit --'}

    def get_queryset(self):
        return ArchivalUnit.objects.filter(level='S')

    def label_from_instance(self, obj):
        return '<span class="archival_unit_title level_' + obj.level + '">' + obj.title_full + '</span>'
