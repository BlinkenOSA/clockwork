from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import ProtectedError
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import FormView, CreateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxUpdateView

from archival_unit.models import ArchivalUnit
from container.forms import ContainerForm, ContainerUpdateForm
from container.models import Container
from finding_aids.models import FindingAidsEntity


class ContainerList(FormView):
    template_name = 'container/list.html'
    form_class = ContainerForm

    def get_context_data(self, **kwargs):
        context = super(ContainerList, self).get_context_data(**kwargs)
        archival_unit = ArchivalUnit.objects.get(pk=self.kwargs['archival_unit'])
        context['archival_unit'] = archival_unit
        archival_unit_names = archival_unit.title_full.split(": ")
        context['fonds_name'] = archival_unit_names[0].replace(archival_unit.reference_code, "").strip()
        context['subfonds_name'] = archival_unit_names[1]
        context['series_name'] = archival_unit_names[2]
        return context


class ContainerListJson(BaseDatatableView):
    model = Container
    columns = ['container_no', 'identifier', 'carrier_type', 'primary_type', 'container_label',
               'number_of_fa_entities', 'navigate', 'action']
    order_columns = ['primary_type', 'container_no']
    max_display_length = 500

    def get_initial_queryset(self):
        if self.kwargs['archival_unit'] == '0':
            container = Container.objects.none()
        else:
            archival_unit = ArchivalUnit.objects.get(pk=self.kwargs['archival_unit'])
            container = Container.objects.filter(archival_unit=archival_unit).order_by('container_no')
        return container

    def render_column(self, row, column):
        if column == 'primary_type':
            return row.primary_type.type
        elif column == 'container_no':
            return '%s/%s' % (row.archival_unit.reference_code, row.container_no)
        elif column == 'identifier':
            if row.legacy_id:
                return "%s (%s)" % (row.permanent_id, row.legacy_id)
            else:
                return row.permanent_id
        elif column == 'carrier_type':
            return row.carrier_type.type
        elif column == 'number_of_fa_entities':
            return FindingAidsEntity.objects.filter(container__id=row.id).count()
        elif column == 'navigate':
            return render_to_string(template_name='container/table_navigate_buttons.html', context={'container': row.id})
        elif column == 'action':
            return render_to_string(template_name='container/table_action_buttons.html', context={'container': row.id})
        else:
            return super(ContainerListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class ContainerCreate(CreateView):
    model = Container
    fields = ['archival_unit', 'primary_type', 'carrier_type', 'container_label']

    def form_valid(self, form):
        container = form.instance
        container_number = Container.objects.filter(archival_unit=container.archival_unit).count()
        form.instance.container_no = container_number + 1
        if self.request.is_ajax():
            form.save()
            data = {
                'DT_RowId': container.id,
                'container_no': container.container_no,
                'primary_type': container.primary_type.type,
                'carrier_type': container.carrier_type.type,
                'container_label': container.container_label,
                'number_of_fa_entities': 0,
                'action': render_to_string('container/table_action_buttons.html', context={'container': container.id}),
                'navigate': render_to_string('container/table_navigate_buttons.html', context={'container': container.id})
            }
            return JsonResponse(data)
        else:
            return super(ContainerCreate, self).form_valid(form)


class ContainerUpdate(SuccessMessageMixin, AjaxUpdateView):
    model = Container
    form_class = ContainerUpdateForm
    template_name = 'container/form/form_update_container.html'
    success_message = ugettext("Container was updated successfully")


class ContainerDelete(DeleteView):
    model = Container
    template_name = 'container/delete.html'
    context_object_name = 'container'
    success_message = ugettext("Container was deleted successfully")

    def get_success_url(self):
        archival_unit = self.object.archival_unit
        return reverse_lazy('container:list_with_archival_unit', kwargs={'archival_unit': archival_unit.id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        try:
            return super(ContainerDelete, self).delete(request, *args, **kwargs)
        except ProtectedError:
            return HttpResponseRedirect(self.get_success_url())
