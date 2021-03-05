import json
import os

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils import dateformat
from pyreportjasper import JasperPy

from archival_unit.models import ArchivalUnit
from container.models import Container
from finding_aids.mixins import FindingAidsPermissionMixin
from django.http import HttpResponse, HttpResponseNotFound

from finding_aids.models import FindingAidsEntity
from isad.models import Isad


class FindingAidsLabelDataView(FindingAidsPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        archival_unit = get_object_or_404(ArchivalUnit, pk=kwargs['series_id'])

        self.make_json(kwargs['series_id'])
        self.create_report(archival_unit.reference_code_id)

        filename = '%s_labels.pdf' % archival_unit.reference_code_id
        file_path = os.path.join(settings.BASE_DIR, 'clockwork', 'labels', 'output', filename)
        if os.path.exists(file_path):
            with open(file_path, 'r') as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename="%s"' % filename
                return response
        else:
            return HttpResponseNotFound('The requested pdf was not found in our server.')

    def make_json(self, series_id):
        json_array = []

        archival_unit = get_object_or_404(ArchivalUnit, pk=series_id)
        containers = Container.objects.filter(archival_unit=archival_unit)

        for container in containers:
            label = {}
            label['f'] = archival_unit.fonds
            label['sf'] = archival_unit.subfonds
            label['s'] = archival_unit.series
            label['boxNo'] = container.container_no
            label['fondName'] = archival_unit.get_fonds().title
            label['subFondName'] = archival_unit.get_subfonds().title
            label['series'] = archival_unit.title

            start_folder = FindingAidsEntity.objects.filter(container=container).order_by('folder_no',
                                                                                          'sequence_no').first()
            last_folder = FindingAidsEntity.objects.filter(container=container).order_by('folder_no',
                                                                                         'sequence_no').last()

            if start_folder and last_folder:
                label['startFolderName'] = start_folder.title
                label['startFolderDate'] = self._encode_date(start_folder.date_from)
                label['lastFolderName'] = last_folder.title
                label['lastFolderDate'] = self._encode_date(last_folder.date_from)

            isad = Isad.objects.filter(archival_unit=archival_unit).first()
            if isad:
                label['restrictionText'] = isad.access_rights.statement if isad.access_rights else ''
            else:
                label['restrictionText'] = 'Unknown'
            json_array.append(label)

        output_file = os.path.join(settings.BASE_DIR, 'clockwork', 'labels', 'workdir', '%s.json' % archival_unit.reference_code_id)
        with open(output_file, 'w') as outfile:
            json.dump({'labels': json_array}, outfile, indent=4)

    def _encode_date(self, date):
        if date.year and date.month and date.day:
            return dateformat.format(date, 'd M, Y')
        elif date.year and date.month:
            return dateformat.format(date, 'M, Y')
        elif date.year:
            return dateformat.format(date, 'Y')

    def create_report(self, reference_code):
        input_file = os.path.join(settings.BASE_DIR, 'clockwork', 'labels', 'jasper', 'labels_4.jrxml')
        output_file = os.path.join(settings.BASE_DIR, 'clockwork', 'labels', 'output', '%s_labels' % reference_code)
        data_file = os.path.join(settings.BASE_DIR, 'clockwork', 'labels', 'workdir', '%s.json' % reference_code)

        jasper = JasperPy()
        jasper.process(
            input_file,
            output_file=output_file,
            format_list=["pdf"],
            parameters={},
            db_connection={
                'data_file': data_file,
                'driver': 'json',
                'json_query': 'labels',
            },
            locale='en_US'
        )