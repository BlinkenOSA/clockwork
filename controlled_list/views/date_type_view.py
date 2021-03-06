from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from clockwork.mixins import GeneralAllPermissionMixin
from controlled_list.forms import DateTypeForm
from controlled_list.models import DateType


class DateTypePermissionMixin(GeneralAllPermissionMixin):
    permission_model = DateType


class DateTypeList(DateTypePermissionMixin, TemplateView):
    template_name = 'controlled_list/date_type/list.html'


class DateTypeListJson(DateTypePermissionMixin, BaseDatatableView):
    model = DateType
    columns = ['id', 'type', 'action']
    order_columns = ['type']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(type__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('controlled_list/date_type/table_action_buttons.html', context={'id': row.id})
        else:
            return super(DateTypeListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class DateTypeCreate(DateTypePermissionMixin, AjaxCreateView):
    form_class = DateTypeForm
    model = DateType
    template_name = 'controlled_list/date_type/form.html'

    def get_response_message(self):
        return ugettext("DateType: %s was created successfully!") % self.object


class DateTypeUpdate(DateTypePermissionMixin, AjaxUpdateView):
    form_class = DateTypeForm
    model = DateType
    template_name = 'controlled_list/date_type/form.html'

    def get_response_message(self):
        return ugettext("DateType: %s was updated successfully!") % self.object
