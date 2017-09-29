from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from clockwork.mixins import GeneralAllPermissionMixin
from controlled_list.forms import ExtentUnitForm
from controlled_list.models import ExtentUnit


class ExtentUnitPermissionMixin(GeneralAllPermissionMixin):
    permission_model = ExtentUnit


class ExtentUnitList(ExtentUnitPermissionMixin, TemplateView):
    template_name = 'controlled_list/extent_unit/list.html'


class ExtentUnitListJson(ExtentUnitPermissionMixin, BaseDatatableView):
    model = ExtentUnit
    columns = ['id', 'unit', 'action']
    order_columns = ['unit']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(unit__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('controlled_list/extent_unit/table_action_buttons.html', context={'id': row.id})
        else:
            return super(ExtentUnitListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class ExtentUnitCreate(ExtentUnitPermissionMixin, AjaxCreateView):
    form_class = ExtentUnitForm
    model = ExtentUnit
    template_name = 'controlled_list/extent_unit/form.html'

    def get_response_message(self):
        return ugettext("ExtentUnit: %s was created successfully!") % self.object


class ExtentUnitUpdate(ExtentUnitPermissionMixin, AjaxUpdateView):
    form_class = ExtentUnitForm
    model = ExtentUnit
    template_name = 'controlled_list/extent_unit/form.html'

    def get_response_message(self):
        return ugettext("ExtentUnit: %s was updated successfully!") % self.object
