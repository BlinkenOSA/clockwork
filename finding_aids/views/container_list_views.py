from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from container.models import Container
from finding_aids.models import FindingAidsEntity


class FindingAidsInContainerList(TemplateView):
    template_name = 'finding_aids/container_view/list.html'

    def get_context_data(self, **kwargs):
        context = super(FindingAidsInContainerList, self).get_context_data(**kwargs)
        container = Container.objects.get(pk=self.kwargs['container_id'])
        context['container'] = container
        context['templates'] = FindingAidsEntity.objects.filter(is_template=True,
                                                                archival_unit=container.archival_unit)\
            .order_by('template_name')
        return context


class FindingAidsInContainerListJson(BaseDatatableView):
    model = FindingAidsEntity
    columns = ['level', 'title', 'title_original', 'date', 'action']
    order_columns = ['folder_no', 'sequence_no', 'title']
    max_display_length = 500

    def get_initial_queryset(self):
        container = Container.objects.get(pk=self.kwargs['container_id'])
        finding_aids_entities = FindingAidsEntity.objects.filter(container=container).order_by('folder_no')
        return finding_aids_entities

    def render_column(self, row, column):
        if column == 'level':
            folder_no = row.container.archival_unit.reference_code + '/' + str(row.container.container_no) + \
                        ':' + str(row.folder_no)
            if row.level == 'F':
                icon = '<i class="fa fa-folder-open-o"></i>'
                return '<span class="call_no_folder">' + icon + folder_no + '</span>'
            else:
                icon = '<i class="fa fa-file-o"></i>'
                return '<span class="call_no_item">' + icon + folder_no + '-' + str(row.sequence_no) + '</span>'
        elif column == 'date':
            dates = [str(row.date_from) if row.date_from else "", str(row.date_to) if row.date_to else ""]
            return ' - '.join(filter(None, dates))
        elif column == 'action':
            return render_to_string('finding_aids/container_view/table_action_buttons.html', context={
                'container_id': row.container_id, 'id': row.id})
        else:
            return super(FindingAidsInContainerListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array