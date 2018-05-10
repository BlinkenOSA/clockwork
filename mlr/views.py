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
    columns = ['id', 'series', 'quantity', 'carrier_type', 'size', 'mrss', 'action']
    order_columns = ['series__sort', ['carrier_type', 'series__sort']]
    max_display_length = 500

    def get_initial_queryset(self):
        qs = MLREntity.objects.all().order_by('series__sort')

        fonds = self.request.GET['fonds'] if 'fonds' in self.request.GET.keys() else ""

        row = self.request.GET['row'] if 'row' in self.request.GET.keys() else ""
        module = self.request.GET['module'] if 'module' in self.request.GET.keys() else ""
        section = self.request.GET['section'] if 'section' in self.request.GET.keys() else ""
        shelf = self.request.GET['shelf'] if 'shelf' in self.request.GET.keys() else ""

        if fonds:
            fonds = ArchivalUnit.objects.get(pk=fonds)
            archival_units = ArchivalUnit.objects.filter(level='S', fonds=fonds.fonds)
            qs = qs.filter(series__in=archival_units).order_by('series__sort')

        if module:
            qs = qs.filter(locations__module=module)

        if row:
            qs = qs.filter(locations__row=row)

        if section:
            qs = qs.filter(locations__section=section)

        if shelf:
            qs = qs.filter(locations__shelf=shelf)

        return qs

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
        elif column == 'quantity':
            return row.get_count()
        elif column == 'size':
            return row.get_size()
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
        qs = MLREntity.objects.all().order_by('series__sort', 'carrier_type__type')
        file_name = 'mlr'

        if 'fonds_id' in request.GET:
            archival_unit = ArchivalUnit.objects.get(id=request.GET['fonds_id'])
            qs = qs.filter(series__level='S',
                                            series__fonds=archival_unit.fonds).order_by('series__sort',
                                                                                        'carrier_type__type')
            file_name += "-hu_osa_%s" % archival_unit.fonds

        if 'module' in request.GET:
            qs = qs.filter(locations__module=request.GET['module'])
            file_name += "-module_%s" % request.GET['module']

        if 'row' in request.GET:
            qs = qs.filter(locations__module=request.GET['row'])
            file_name += "-row_%s" % request.GET['row']

        if 'section' in request.GET:
            qs = qs.filter(locations__module=request.GET['section'])
            file_name += "-section_%s" % request.GET['section']

        if 'shelf' in request.GET:
            qs = qs.filter(locations__module=request.GET['shelf'])
            file_name += "-shelf_%s" % request.GET['shelf']

        file_name += ".csv"

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name

        field_names = ['series', 'carrier', 'locations']

        writer = csv.DictWriter(response, delimiter=str(u";"), fieldnames=field_names)
        writer.writeheader()

        for mlr in qs:
            writer.writerow({
                'series': mlr.series.reference_code,
                'carrier': mlr.carrier_type.type,
                'locations': mlr.get_locations()
            })

        return response
