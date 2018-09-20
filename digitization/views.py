# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.template.loader import render_to_string
from django.views.generic import TemplateView, DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView

from container.models import Container


class DigitizationList(LoginRequiredMixin, TemplateView):
    template_name = 'digitization/list.html'


class DigitizationListJson(LoginRequiredMixin, BaseDatatableView):
    model = Container
    columns = ['id', 'container_no', 'barcode', 'digital_version_creation_date', 'duration', 'carrier_type', 'action']
    order_columns = ['container_no', 'barcode', 'digital_version_creation_date', 'duration', 'carrier_type']

    def get_initial_queryset(self):
        qs = Container.objects.filter(digital_version_exists=True)
        return qs

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(archival_unit__reference_code__icontains=search) |
                Q(barcode__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'container_no':
            return '%s/%s' % (row.archival_unit.reference_code, row.container_no)
        elif column == 'carrier_type':
            return row.carrier_type.type
        elif column == 'duration':
            duration = ""
            tech_md = row.digital_version_technical_metadata
            if tech_md:
                tech_md = json.loads(tech_md)
                for stream in tech_md['streams']:
                    if stream.get('codec_type') == 'video':
                        seconds = float(stream.get('duration'))
                        total_seconds = datetime.timedelta(seconds=seconds).total_seconds()
                        hours, remainder = divmod(total_seconds,60*60)
                        minutes, seconds = divmod(remainder,60)
                        return "%02d:%02d:%02d" % (hours, minutes, seconds)
            return duration
        elif column == 'action':
            tech_md_exists = True if row.digital_version_technical_metadata else False
            return render_to_string('digitization/table_action_buttons.html',
                                    context={'id': row.id, 'tech_md_exists': tech_md_exists})
        else:
            return super(DigitizationListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class DigitizationTechnicalMetadata(LoginRequiredMixin, DetailView):
    model = Container
    template_name = 'digitization/technical_metadata.html'
    context_object_name = 'container'
