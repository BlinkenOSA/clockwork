from django.views.generic import FormView
from django_datatables_view.base_datatable_view import BaseDatatableView

from container.models import Container
from finding_aids.forms import FindingAidsArchivalUnitForm, FindingAidsInContainerForm
from finding_aids.models import FindingAidsEntity


class FindingAidsArchivalUnit(FormView):
    template_name = 'finding_aids/select_archival_unit/select_archival_unit.html'
    form_class = FindingAidsArchivalUnitForm


class FindingAidsInContainerList(FormView):
    template_name = 'finding_aids/container_view/list.html'
    form_class = FindingAidsInContainerForm

    def get_context_data(self, **kwargs):
        context = super(FindingAidsInContainerList, self).get_context_data(**kwargs)
        container = Container.objects.get(pk=self.kwargs['container_id'])
        context['container'] = container
        archival_unit = container.archival_unit
        context['archival_unit'] = archival_unit
        archival_unit_names = archival_unit.title_full.split(": ")
        context['fonds_name'] = archival_unit_names[0].replace(archival_unit.reference_code, "").strip()
        context['subfonds_name'] = archival_unit_names[1]
        context['series_name'] = archival_unit_names[2]
        return context


class FindingAidsInContainerListJson(BaseDatatableView):
    model = FindingAidsEntity
    columns = ['entity_no', 'title', 'title_original', 'date_from', 'date_to']
    order_columns = ['entity_no', 'title']
    max_display_length = 500

    def get_initial_queryset(self):
        container = Container.objects.get(pk=self.kwargs['container_id'])
        finding_aids_entities = FindingAidsEntity.objects.filter(container=container).order_by('entity_no')
        return finding_aids_entities

    def render_column(self, row, column):
        return super(FindingAidsContainerListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array
