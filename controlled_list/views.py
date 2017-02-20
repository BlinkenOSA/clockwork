from django.db.models import Q
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from json_views.views import JSONDataView

from controlled_list.models import CarrierType, PrimaryType, Building


class BuildingList(TemplateView):
    template_name = 'controlled_list/building/list.html'


class BuildingListJson(BaseDatatableView):
    model = Building
    columns = ['building']
    order_columns = ['building']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(building__icontains=search)
            )
        return qs


class PrimaryTypeJSONList(JSONDataView):
    def get_context_data(self, **kwargs):
        context = super(PrimaryTypeJSONList, self).get_context_data(**kwargs)
        context_pieces = []
        primaryTypes = PrimaryType.objects.all()

        for primaryType in primaryTypes:
            context_pieces.append({"label": primaryType.type, "value": primaryType.id})
        context["primaryTypes"] = context_pieces

        return context


class CarrierTypeJSONList(JSONDataView):
    def get_context_data(self, **kwargs):
        context = super(CarrierTypeJSONList, self).get_context_data(**kwargs)
        context_pieces = []
        carrierTypes = CarrierType.objects.all()

        for carrierType in carrierTypes:
            context_pieces.append({"label": carrierType.type, "value": carrierType.id})
        context["carrierTypes"] = context_pieces

        return context

