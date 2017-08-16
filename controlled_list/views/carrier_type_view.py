from json_views.views import JSONDataView

from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from controlled_list.forms import CarrierTypeForm
from controlled_list.models import CarrierType


class CarrierTypeList(TemplateView):
    template_name = 'controlled_list/carrier_type/list.html'


class CarrierTypeListJson(BaseDatatableView):
    model = CarrierType
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
            return render_to_string('controlled_list/carrier_type/table_action_buttons.html', context={'id': row.id})
        else:
            return super(CarrierTypeListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class CarrierTypeCreate(AjaxCreateView):
    form_class = CarrierTypeForm
    model = CarrierType
    template_name = 'controlled_list/carrier_type/form.html'

    def get_response_message(self):
        return ugettext("CarrierType: %s was created successfully!") % self.object


class CarrierTypeUpdate(AjaxUpdateView):
    form_class = CarrierTypeForm
    model = CarrierType
    template_name = 'controlled_list/carrier_type/form.html'

    def get_response_message(self):
        return ugettext("CarrierType: %s was updated successfully!") % self.object


class CarrierTypeJSONList(JSONDataView):
    def get_context_data(self, **kwargs):
        context = super(CarrierTypeJSONList, self).get_context_data(**kwargs)
        context_pieces = []
        carrierTypes = CarrierType.objects.all()

        for carrierType in carrierTypes:
            context_pieces.append({"label": carrierType.type, "value": carrierType.id})
        context["carrierTypes"] = context_pieces

        return context