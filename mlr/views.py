# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView, FormView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxUpdateView

from archival_unit.models import ArchivalUnit
from clockwork.mixins import GeneralAllPermissionMixin
from mlr.forms import MLRForm, MLRListForm
from mlr.models import MLREntity


class MLRPermissionMixin(GeneralAllPermissionMixin):
    permission_model = MLREntity


class MLRList(MLRPermissionMixin, FormView):
    template_name = "mlr/list.html"
    form_class = MLRListForm


class MLRListJson(MLRPermissionMixin, BaseDatatableView):
    model = MLREntity
    columns = ['id', 'series', 'carrier_type', 'building', 'mrss', 'action']
    order_columns = ['series__sort', ['carrier_type', 'series__sort']]
    max_display_length = 500

    def get_initial_queryset(self):
        fonds = self.request.GET['fonds'] if 'fonds' in self.request.GET.keys() else ""

        if fonds:
            fonds = ArchivalUnit.objects.get(pk=fonds)
            archival_units = ArchivalUnit.objects.filter(level='S', fonds=fonds.fonds)
            return MLREntity.objects.filter(series__in=archival_units).order_by('series__sort')
        else:
            return MLREntity.objects.all().order_by('series__sort')

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(series__reference_code__icontains=search) |
                Q(carrier_type__type__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'series':
            return row.series.reference_code
        if column == 'building':
            return row.building.building if row.building else ""
        elif column == 'carrier_type':
            return row.carrier_type.type if row.carrier_type else ""
        elif column == 'mrss':
            module = str(row.module) if row.module else "-"
            r = str(row.row) if row.row else "-"
            section = str(row.section) if row.section else "-"
            shelf = str(row.shelf) if row.shelf else "-"
            return "%s / %s / %s / %s" % (module, r, section, shelf)
        elif column == 'action':
            return render_to_string('mlr/table_action_buttons.html',
                                    context={'id': row.id})
        else:
            return super(MLRListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class MLRUpdate(MLRPermissionMixin, AjaxUpdateView):
    model = MLREntity
    form_class = MLRForm
    template_name = 'mlr/form.html'

    def get_response_message(self):
        return ugettext("MLR was updated successfully!")
