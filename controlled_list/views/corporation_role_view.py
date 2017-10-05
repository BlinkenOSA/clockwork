from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from clockwork.mixins import GeneralAllPermissionMixin, AuditTrailContextMixin
from controlled_list.forms import CorporationRoleForm
from controlled_list.models import CorporationRole


class CorporationRolePermissionMixin(GeneralAllPermissionMixin):
    permission_model = CorporationRole


class CorporationRoleList(CorporationRolePermissionMixin, TemplateView):
    template_name = 'controlled_list/corporation_role/list.html'


class CorporationRoleListJson(CorporationRolePermissionMixin, BaseDatatableView):
    model = CorporationRole
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
            return render_to_string('controlled_list/corporation_role/table_action_buttons.html', context={'id': row.id})
        else:
            return super(CorporationRoleListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class CorporationRoleCreate(CorporationRolePermissionMixin, AjaxCreateView):
    form_class = CorporationRoleForm
    model = CorporationRole
    template_name = 'controlled_list/corporation_role/form.html'

    def get_response_message(self):
        return ugettext("CorporationRole: %s was created successfully!") % self.object


class CorporationRoleUpdate(CorporationRolePermissionMixin, AuditTrailContextMixin, AjaxUpdateView):
    form_class = CorporationRoleForm
    model = CorporationRole
    template_name = 'controlled_list/corporation_role/form.html'

    def get_response_message(self):
        return ugettext("CorporationRole: %s was updated successfully!") % self.object
