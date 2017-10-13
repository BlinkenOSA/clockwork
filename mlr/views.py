# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxUpdateView

from clockwork.mixins import GeneralAllPermissionMixin
from mlr.forms import MLRForm
from mlr.models import MLREntity


class MLRPermissionMixin(GeneralAllPermissionMixin):
    permission_model = MLREntity


class MLRList(MLRPermissionMixin, TemplateView):
    template_name = 'mlr/list.html'


class MLRListJson(MLRPermissionMixin, BaseDatatableView):
    model = MLREntity
    columns = ['id', 'series', 'carrier_type', 'building', 'module', 'row', 'section', 'shelf', 'action']
    order_columns = ['id', 'series', 'carrier_type']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(series__icontains=search) |
                Q(carrier_type__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'series':
            return row.series.reference_code
        if column == 'building':
            return row.building.building if row.building else ""
        elif column == 'carrier_type':
            return row.carrier_type.type if row.carrier_type else ""
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
