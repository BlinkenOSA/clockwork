from django.shortcuts import get_object_or_404
from django.views import View
from django.utils import dateformat

from archival_unit.models import ArchivalUnit
from container.models import Container
from finding_aids.mixins import FindingAidsPermissionMixin
from django.http import JsonResponse

from finding_aids.models import FindingAidsEntity
from isad.models import Isad


class FindingAidsLabelDataView(FindingAidsPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        json_array = []
        archival_unit = get_object_or_404(ArchivalUnit, pk=kwargs['series_id'])
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

            start_folder = FindingAidsEntity.objects.filter(container=container).order_by('folder_no', 'sequence_no').first()
            last_folder = FindingAidsEntity.objects.filter(container=container).order_by('folder_no', 'sequence_no').last()

            if start_folder and last_folder:
                label['startFolderName'] = start_folder.title
                label['startFolderDate'] = self.encode_date(start_folder.date_from)
                label['lastFolderName'] = last_folder.title

                if last_folder.date_to == '':
                    label['lastFolderDate'] = self.encode_date(last_folder.date_from)
                else:
                    label['lastFolderDate'] = self.encode_date(last_folder.date_to)

            isad = Isad.objects.get(archival_unit=archival_unit)
            label['restrictionText'] = isad.access_rights.statement if isad.access_rights else ''
            json_array.append(label)
        return JsonResponse(json_array, safe=False)

    def encode_date(self, date):
        if date.year and date.month and date.day:
            return dateformat.format(date, 'd M, Y')
        elif date.year and date.month:
            return dateformat.format(date, 'M, Y')
        elif date.year:
            return dateformat.format(date, 'Y')