from django.views.generic import ListView
from fm.views import JSONResponseMixin

from container.models import Container
from finding_aids.models import FindingAidsEntity
from finding_aids.views.helper_functions import get_number_of_folders, get_number_of_items


class FindingAidsNewFolderNumber(JSONResponseMixin, ListView):
    model = FindingAidsEntity

    def get(self, request, *args, **kwargs):
        stats = {}

        folder_no = get_number_of_folders(kwargs['container_id'])

        container = Container.objects.get(pk=kwargs['container_id'])
        arc = "%s/%s:%s" % (container.archival_unit.reference_code,
                            container.container_no,
                            folder_no + 1)

        stats['new_folder'] = folder_no + 1
        stats['new_arc'] = arc
        return self.render_json_response({'stats': stats})


class FindingAidsNewItemNumber(JSONResponseMixin, ListView):
    model = FindingAidsEntity

    def get(self, request, *args, **kwargs):
        stats = {}
        item_no = get_number_of_items(kwargs['container_id'], kwargs['folder_no'])

        container = Container.objects.get(pk=kwargs['container_id'])
        arc = "%s/%s:%s-%s" % (container.archival_unit.reference_code,
                               container.container_no,
                               kwargs['folder_no'],
                               item_no + 1)

        stats['new_item'] = item_no + 1
        stats['new_arc'] = arc
        return self.render_json_response({'stats': stats})