from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from clockwork.mixins import GeneralAllPermissionMixin, AuditTrailContextMixin
from controlled_list.forms import PersonRoleForm
from controlled_list.models import PersonRole


class PersonRolePermissionMixin(GeneralAllPermissionMixin):
    permission_model = PersonRole


class PersonRoleList(PersonRolePermissionMixin, TemplateView):
    template_name = 'controlled_list/person_role/list.html'


class PersonRoleListJson(PersonRolePermissionMixin, BaseDatatableView):
    model = PersonRole
    columns = ['id', 'role', 'action']
    order_columns = ['role']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(role__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('controlled_list/person_role/table_action_buttons.html', context={'id': row.id})
        else:
            return super(PersonRoleListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class PersonRoleCreate(PersonRolePermissionMixin, AjaxCreateView):
    form_class = PersonRoleForm
    model = PersonRole
    template_name = 'controlled_list/person_role/form.html'

    def get_response_message(self):
        return ugettext("PersonRole: %s was created successfully!") % self.object.role

    def get_success_result(self):
        results = super(PersonRoleCreate, self).get_success_result()
        results['entry_id'] = self.object.id,
        results['entry_name'] = self.object.role
        return results


class PersonRoleUpdate(PersonRolePermissionMixin, AuditTrailContextMixin, AjaxUpdateView):
    form_class = PersonRoleForm
    model = PersonRole
    template_name = 'controlled_list/person_role/form.html'

    def get_response_message(self):
        return ugettext("PersonRole: %s was updated successfully!") % self.object.role
