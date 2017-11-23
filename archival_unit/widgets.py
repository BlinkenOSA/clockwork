from django_select2.forms import ModelSelect2Widget

from archival_unit.models import ArchivalUnit
from finding_aids.models import FindingAidsEntity


class ArchivalUnitFondsSelect2Widget(ModelSelect2Widget):
    search_fields = ['title__icontains', 'reference_code__icontains']
    attrs = {'placeholder': '-- Select Fonds --'}

    def get_queryset(self):
        return ArchivalUnit.objects.filter(level='F')

    def label_from_instance(self, obj):
        return obj.title_full


class ArchivalUnitSeriesContainersSelect2Widget(ModelSelect2Widget):
    search_fields = ['title__icontains', 'reference_code__icontains']
    attrs = {'placeholder': '-- Select Fonds --'}

    def get_queryset(self):
        return ArchivalUnit.objects.filter(level='S')

    def label_from_instance(self, obj):
        finding_aids_count = FindingAidsEntity.objects.filter(container__in=obj.container_set.all()).count()
        countainer_count = obj.container_set.count()

        if finding_aids_count == 0:
            finding_aids_message = 'no folder/item'
        elif finding_aids_count == 1:
            finding_aids_message = '1 folder/item'
        else:
            finding_aids_message = '%d folders/items' % finding_aids_count

        if countainer_count == 0:
            return '%s <span class="label label-warning label-container">no containers</span>' % obj
        elif countainer_count == 1:
            return '%s <span class="label label-warning label-container">%s in %d container</span>' % \
                   (obj.title_full, finding_aids_message, countainer_count)
        else:
            return '%s <span class="label label-warning label-container">%s in %d containers</span>' % \
                   (obj.title_full, finding_aids_message, countainer_count)
