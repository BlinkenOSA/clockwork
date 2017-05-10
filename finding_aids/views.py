from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import FormView, ListView, TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView, JSONResponseMixin

from container.models import Container
from finding_aids.forms import FindingAidsArchivalUnitForm, FindingAidsInContainerForm, FindingAidsInContainerCreateForm, \
    FindingAidsInContainerUpdateForm
from finding_aids.models import FindingAidsEntity


class FindingAidsArchivalUnit(FormView):
    template_name = 'finding_aids/select_archival_unit/select_archival_unit.html'
    form_class = FindingAidsArchivalUnitForm


class FindingAidsInContainerList(TemplateView):
    template_name = 'finding_aids/container_view/list.html'

    def get_context_data(self, **kwargs):
        context = super(FindingAidsInContainerList, self).get_context_data(**kwargs)
        context['container'] = Container.objects.get(pk=kwargs['container_id'])
        return context


class FindingAidsInContainerListJson(BaseDatatableView):
    model = FindingAidsEntity
    columns = ['level', 'title', 'title_original', 'date', 'action']
    order_columns = ['folder_no', 'item_no', 'title']
    max_display_length = 500

    def get_initial_queryset(self):
        container = Container.objects.get(pk=self.kwargs['container_id'])
        finding_aids_entities = FindingAidsEntity.objects.filter(container=container).order_by('folder_no')
        return finding_aids_entities

    def render_column(self, row, column):
        if column == 'level':
            folder_no = row.container.archival_unit.reference_code + '/' + str(row.folder_no)
            if row.level == 'F':
                icon = '<i class="fa fa-folder-open-o"></i>'
                return '<span class="call_no_folder">' + icon + folder_no + '</span>'
            else:
                icon = '<i class="fa fa-file-o"></i>'
                return '<span class="call_no_item">' + icon + folder_no + ':' + str(row.item_no) + '</span>'
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


class FindingAidsQuickCreate(SuccessMessageMixin, AjaxCreateView):
    model = FindingAidsEntity
    form_class = FindingAidsInContainerCreateForm
    template_name = 'finding_aids/container_view/form/quick_create.html'
    success_message = ugettext("Folder/Item was created successfully")

    def get_initial(self):
        initial = super(FindingAidsQuickCreate, self).get_initial()
        initial = initial.copy()
        initial['container_name'] = Container.objects.get(pk=self.kwargs['container_id'])
        return initial

    def get_form(self, form_class=None):
        form = super(FindingAidsQuickCreate, self).get_form()
        form.fields['folder_no'].choices = \
            [(n, n) for n in range(1, get_number_of_folders(self.kwargs['container_id']) + 1)]
        return form

    def pre_save(self):
        self.object.container = Container.objects.get(pk=self.kwargs['container_id'])


class FindingAidsQuickUpdate(SuccessMessageMixin, AjaxUpdateView):
    model = FindingAidsEntity
    form_class = FindingAidsInContainerUpdateForm
    template_name = 'finding_aids/container_view/form/quick_update.html'
    success_message = ugettext("Folder/Item was updated successfully")

    def get_initial(self):
        initial = super(FindingAidsQuickUpdate, self).get_initial()
        initial = initial.copy()
        initial['container_name'] = Container.objects.get(pk=self.kwargs['container_id'])
        return initial

    def get_form(self, form_class=None):
        form = super(FindingAidsQuickUpdate, self).get_form()
        return form


class FindingAidsFoldersItemsStatistics(JSONResponseMixin, ListView):
    model = FindingAidsEntity

    def get(self, request, *args, **kwargs):
        stats = {}
        folder_no = get_number_of_folders(kwargs['container_id'])

        for folder in range(1, folder_no + 1):
            item_no = get_number_of_items(kwargs['container_id'], folder)
            stats[folder] = item_no

        stats[folder_no + 1] = 0
        return self.render_json_response({'stats': stats})


def get_number_of_folders(container_id):
    return FindingAidsEntity.objects.filter(container=Container.objects.get(pk=container_id))\
                                    .values('folder_no').distinct().count()


def get_number_of_items(container_id, folder_no):
    return FindingAidsEntity.objects.filter(level='I')\
        .filter(container=Container.objects.get(pk=container_id))\
        .filter(folder_no=folder_no)\
        .count()
