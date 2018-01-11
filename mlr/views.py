# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv

from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import FormView, View
from django_datatables_view.base_datatable_view import BaseDatatableView
from extra_views import NamedFormsetsMixin
from fm.views import AjaxUpdateView

from archival_unit.models import ArchivalUnit
from clockwork.inlineform import UpdateWithInlinesAjaxView
from clockwork.mixins import GeneralAllPermissionMixin
from mlr.forms import MLRForm, MLRListForm, MLRLocationInline
from mlr.models import MLREntity


class MLRPermissionMixin(GeneralAllPermissionMixin):
    permission_model = MLREntity


class MLRList(MLRPermissionMixin, FormView):
    template_name = "mlr/list.html"
    form_class = MLRListForm


class MLRListJson(MLRPermissionMixin, BaseDatatableView):
    model = MLREntity
    columns = ['id', 'series', 'carrier_type', 'mrss', 'action']
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
        elif column == 'carrier_type':
            return row.carrier_type.type if row.carrier_type else ""
        elif column == 'mrss':
            return row.get_locations()
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


class MLRUpdate(MLRPermissionMixin, NamedFormsetsMixin, UpdateWithInlinesAjaxView):
    model = MLREntity
    form_class = MLRForm
    template_name = 'mlr/form.html'
    inlines = [MLRLocationInline]
    inlines_names = ['mlr_locations']

    def get_initial(self):
        initial = super(MLRUpdate, self).get_initial()
        initial['series_name'] = self.object.series
        initial['carrier_type_name'] = self.object.carrier_type
        return initial

    def get_response_message(self):
        return ugettext("MLR was updated successfully!")


class MLRExportCSV(View):
    def get(self, request, *args, **kwargs):
        if 'fonds_id' in request.GET:
            archival_unit = ArchivalUnit.objects.get(id=request.GET['fonds_id'])
            mlr_records = MLREntity.objects.filter(series__level='S',
                                                   series__fonds=archival_unit.fonds).order_by('series__sort',
                                                                                               'carrier_type__type')
            file_name = "mlr_hu_osa_%s.csv" % archival_unit.fonds
        else:
            mlr_records = MLREntity.objects.all().order_by('series__sort', 'carrier_type__type')
            file_name = 'mlr_all_archival_units.csv'

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name

        field_names = ['series', 'carrier', 'locations']

        writer = csv.DictWriter(response, delimiter=str(u";"), fieldnames=field_names)
        writer.writeheader()

        for mlr in mlr_records:
            writer.writerow({
                'series': mlr.series.reference_code,
                'carrier': mlr.carrier_type.type,
                'locations': mlr.get_locations()
            })

        return response
