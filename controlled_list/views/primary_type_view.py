from json_views.views import JSONDataView

from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from clockwork.mixins import GeneralAllPermissionMixin
from controlled_list.forms import PrimaryTypeForm
from controlled_list.models import PrimaryType


class PrimaryTypePermissionMixin(GeneralAllPermissionMixin):
    permission_model = PrimaryType


class PrimaryTypeList(PrimaryTypePermissionMixin, TemplateView):
    template_name = 'controlled_list/primary_type/list.html'


class PrimaryTypeListJson(PrimaryTypePermissionMixin, BaseDatatableView):
    model = PrimaryType
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
            return render_to_string('controlled_list/primary_type/table_action_buttons.html', context={'id': row.id})
        else:
            return super(PrimaryTypeListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class PrimaryTypeCreate(PrimaryTypePermissionMixin, AjaxCreateView):
    form_class = PrimaryTypeForm
    model = PrimaryType
    template_name = 'controlled_list/primary_type/form.html'

    def get_response_message(self):
        return ugettext("PrimaryType: %s was created successfully!") % self.object


class PrimaryTypeUpdate(PrimaryTypePermissionMixin, AjaxUpdateView):
    form_class = PrimaryTypeForm
    model = PrimaryType
    template_name = 'controlled_list/primary_type/form.html'

    def get_response_message(self):
        return ugettext("PrimaryType: %s was updated successfully!") % self.object


class PrimaryTypeJSONList(PrimaryTypePermissionMixin, JSONDataView):
    def get_context_data(self, **kwargs):
        context = super(PrimaryTypeJSONList, self).get_context_data(**kwargs)
        context_pieces = []
        primaryTypes = PrimaryType.objects.all()

        for primaryType in primaryTypes:
            context_pieces.append({"label": primaryType.type, "value": primaryType.id})
        context["primaryTypes"] = context_pieces

        return context