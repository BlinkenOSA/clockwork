from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from container.models import Container
from finding_aids.models import FindingAidsEntity


class FindingAidsEntityLocationView(APIView):
    permission_classes = []

    def get_archival_unit_data(self, archival_unit):
        return {
            'id': archival_unit.id,
            'catalog_id': archival_unit.isad.catalog_id,
            'key': archival_unit.reference_code.replace(" ", "_").lower(),
            'title': archival_unit.title,
            'title_original': archival_unit.title_original,
            'reference_code': archival_unit.reference_code,
            'level': archival_unit.level,
            'children': []
        }

    def get_container_placeholder(self):
        return {
            'key': 'placeholder',
            'level': 'container'
        }

    def get_container_data(self, container):
        return {
            'key': "%s_%s" % (container.archival_unit.reference_code.replace(" ", "_").lower(), container.container_no),
            'container_no': container.container_no,
            'level': 'container',
            'carrier_type': container.carrier_type.type
        }

    def get_fa_entity_data(self, fa_entity, active=False):
        return {
            'catalog_id': fa_entity.catalog_id,
            'key': fa_entity.archival_reference_code.replace(" ", "_").lower(),
            'reference_code': fa_entity.archival_reference_code,
            'title': fa_entity.title,
            'active': active,
            'level': 'folder' if fa_entity.level == 'F' else 'item'
        }

    def get(self, request, fa_entity_catalog_id):
        tree = []

        fa_entity = get_object_or_404(FindingAidsEntity, catalog_id=fa_entity_catalog_id, archival_unit__isad__published=True)
        series = fa_entity.archival_unit
        subfonds = series.parent
        fonds = subfonds.parent
        container = fa_entity.container

        if hasattr(fonds, 'isad'):
            tree.append(self.get_archival_unit_data(fonds))

        if hasattr(subfonds, 'isad'):
            tree.append(self.get_archival_unit_data(subfonds))

        if hasattr(series, 'isad'):
            tree.append(self.get_archival_unit_data(series))

        # Containers
        container_no = container.container_no
        containers = Container.objects.filter(
            archival_unit=series, container_no__gte=container_no-1, container_no__lte=container_no+1
        ).order_by('container_no')

        for container in containers.iterator():
            tree.append(self.get_container_data(container))

            # Finding Aids Entities
            fa_qs = FindingAidsEntity.objects.filter(container=container).order_by('folder_no', 'sequence_no')

            # Add first FA Entity in container
            fa_first = fa_qs.first()
            fa_last = fa_qs.last()

            tree.append(self.get_fa_entity_data(fa_first, fa_first.archival_reference_code == fa_entity.archival_reference_code))

            if container.container_no == fa_entity.container.container_no and \
               fa_first.archival_reference_code != fa_entity.archival_reference_code and \
               fa_last.archival_reference_code != fa_entity.archival_reference_code:
                tree.append(self.get_fa_entity_data(fa_entity, True))

            if fa_qs.count() > 1:
                tree.append(self.get_fa_entity_data(fa_last, fa_last.archival_reference_code == fa_entity.archival_reference_code))

        return Response(tree)
