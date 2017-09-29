from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from clockwork.mixins import GeneralAllPermissionMixin
from controlled_list.forms import BuildingForm
from controlled_list.models import Building


class BuildingPermissionMixin(GeneralAllPermissionMixin):
    permission_model = Building


class BuildingList(BuildingPermissionMixin, TemplateView):
    template_name = 'controlled_list/building/list.html'


class BuildingListJson(BuildingPermissionMixin, BaseDatatableView):
    model = Building
    columns = ['id', 'building', 'action']
    order_columns = ['building']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(building__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('controlled_list/building/table_action_buttons.html', context={'id': row.id})
        else:
            return super(BuildingListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class BuildingCreate(BuildingPermissionMixin, AjaxCreateView):
    form_class = BuildingForm
    model = Building
    template_name = 'controlled_list/building/form.html'

    def get_response_message(self):
        return ugettext("Building: %s was created successfully!") % self.object


class BuildingUpdate(BuildingPermissionMixin, AjaxUpdateView):
    form_class = BuildingForm
    model = Building
    template_name = 'controlled_list/building/form.html'

    def get_response_message(self):
        return ugettext("Building: %s was updated successfully!") % self.object
