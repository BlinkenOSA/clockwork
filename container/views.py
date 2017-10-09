from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import FormView, CreateView, DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxUpdateView, JSONResponseMixin

from archival_unit.models import ArchivalUnit
from clockwork.ajax_extra_views import AjaxDeleteProtectedView
from clockwork.mixins import GeneralAllPermissionMixin, AuditTrailContextMixin
from container.forms import ContainerForm, ContainerUpdateForm
from container.models import Container
from finding_aids.models import FindingAidsEntity


class ContainerPermissionMixin(GeneralAllPermissionMixin):
    permission_model = Container


class ContainerAllowedArchivalUnitMixin(object):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user.user_profile.allowed_archival_units.count():
            if 'archival_unit' in self.kwargs:
                archival_unit = get_object_or_404(ArchivalUnit, pk=self.kwargs['archival_unit'])
            else:
                container = Container.objects.get(pk=self.kwargs['pk'])
                archival_unit = container.archival_unit

            if archival_unit in user.user_profile.allowed_archival_units.all():
                return super(ContainerAllowedArchivalUnitMixin, self).get(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            return super(ContainerAllowedArchivalUnitMixin, self).get(request, *args, **kwargs)


class ContainerList(ContainerPermissionMixin, ContainerAllowedArchivalUnitMixin, FormView):
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


class ContainerListJson(ContainerPermissionMixin, BaseDatatableView):
    model = Container
    columns = ['container_no', 'identifier', 'carrier_type', 'primary_type', 'container_label',
               'number_of_fa_entities', 'navigate', 'action']
    order_columns = ['primary_type', 'container_no']
    max_display_length = 500
    number_of_fa_entities = 0

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
            self.number_of_fa_entities = FindingAidsEntity.objects.filter(container__id=row.id).count()
            return self.number_of_fa_entities
        elif column == 'navigate':
            return render_to_string(template_name='container/table_navigate_buttons.html', context={'container': row})
        elif column == 'action':
            return render_to_string(template_name='container/table_action_buttons.html',
                                    context={'container': row.id, 'number_of_fa_entities': self.number_of_fa_entities})
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


class ContainerCreate(ContainerPermissionMixin, CreateView):
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
                'navigate': render_to_string('container/table_navigate_buttons.html', context={'container': container})
            }
            return JsonResponse(data)
        else:
            return super(ContainerCreate, self).form_valid(form)


class ContainerUpdate(ContainerPermissionMixin, AuditTrailContextMixin, ContainerAllowedArchivalUnitMixin,
                      SuccessMessageMixin, AjaxUpdateView):
    model = Container
    form_class = ContainerUpdateForm
    template_name = 'container/form/form_update_container.html'
    success_message = ugettext("Container was updated successfully")


class ContainerDelete(ContainerPermissionMixin, ContainerAllowedArchivalUnitMixin, AjaxDeleteProtectedView):
    model = Container
    template_name = 'container/delete.html'
    context_object_name = 'container'
    success_message = ugettext("Container was deleted successfully!")
    error_message = ugettext("Container is not empty, please select an empty one to delete!")


class ContainerAction(ContainerPermissionMixin, ContainerAllowedArchivalUnitMixin, JSONResponseMixin, DetailView):
    model = Container

    def post(self, request, *args, **kwargs):
        action = self.kwargs['action']
        archival_unit = self.kwargs['archival_unit']
        pk = self.kwargs['pk']

        if pk == 'all':
            containers = Container.objects.filter(archival_unit=archival_unit)
        else:
            containers = [self.get_object(),]

        for container in containers:
            finding_aids = FindingAidsEntity.objects.filter(container=container)
            number_of_fa_entities = len(finding_aids)

            if action == 'publish':
                container.publish(request.user)
                for fa in finding_aids:
                    fa.publish(request.user)

            if action == 'unpublish':
                container.unpublish()
                for fa in finding_aids:
                    fa.unpublish()

        if pk == 'all':
            context = {
                'status': 'ok'
            }
        else:
            context = {
                'DT_rowId': container.id,
                'container_no': '%s/%s' % (container.archival_unit.reference_code, container.container_no),
                'primary_type': container.primary_type.type,
                'carrier_type': container.carrier_type.type,
                'identifier': "%s (%s)" % (container.permanent_id, container.legacy_id) if container.legacy_id else container.permanent_id,
                'number_of_fa_entities': number_of_fa_entities,
                'navigate': render_to_string('container/table_navigate_buttons.html', context={'container': container}),
                'action': render_to_string('container/table_action_buttons.html',
                                           context={'container': container.id,
                                                    'number_of_fa_entities': number_of_fa_entities})
            }
        return self.render_json_response(context)

