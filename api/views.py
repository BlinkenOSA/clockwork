# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, \
    get_object_or_404
from rest_framework.views import APIView

from api.permission import APIGroupPermission
from api.serializers.container_serializers import ContainerDigitizedSerializer
from api.serializers.finding_aids_serializer import FindingAidsSerializer, FindingAidsGridSerializer
from container.models import Container
from finding_aids.models import FindingAidsEntity


class GetSetDigitizedContainer(RetrieveUpdateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerDigitizedSerializer
    lookup_field = 'barcode'
    permission_classes = (APIGroupPermission, )


class GetContainerMetadata(ListAPIView):
    serializer_class = FindingAidsSerializer
    lookup_field = 'barcode'
    permission_classes = (APIGroupPermission, )

    def get_queryset(self):
        container = Container.objects.filter(barcode=self.kwargs['barcode']).first()
        if container:
            finding_aids = FindingAidsEntity.objects.filter(container=container, is_template=False)
            return finding_aids


class FindingAidsEntityListView(ListAPIView):
    serializer_class = FindingAidsGridSerializer
    authentication_classes = (SessionAuthentication,)
    pagination_class = None

    def get_queryset(self):
        qs = FindingAidsEntity.objects.filter(archival_unit=self.kwargs['series_id'])\
            .order_by('container__container_no', 'folder_no', 'sequence_no')
        return qs


class FindingAidsEntityView(ListAPIView):
    serializer_class = FindingAidsGridSerializer
    authentication_classes = (SessionAuthentication,)

    def get_queryset(self):
        qs = FindingAidsEntity.objects.filter(archival_unit=self.kwargs['series_id'])\
            .order_by('container__container_no', 'folder_no', 'sequence_no')
        return qs


class FindingAidsEntityUpdateView(UpdateAPIView):
    serializer_class = FindingAidsGridSerializer
    authentication_classes = (SessionAuthentication,)
    queryset = FindingAidsEntity.objects.all()


class GetContainerMetadataByLegacyID(RetrieveAPIView):
    serializer_class = ContainerDigitizedSerializer
    lookup_field = 'barcode'
    permission_classes = (APIGroupPermission, )

    def get_object(self):
        legacy_id = self.kwargs['legacy_id']

        fa_objects = FindingAidsEntity.objects.filter(legacy_id=legacy_id)
        if fa_objects.count() > 0:
            fa_object = fa_objects.first()
            return fa_object.container
        else:
            if re.match(r'^HU OSA [0-9]+-[0-9]+-[0-9]*_[0-9]{3}', legacy_id):
                legacy_id = legacy_id.replace("HU OSA ", "")
                fonds, subfonds, rest = legacy_id.split('-')
                series, container_no = rest.split('_')
                container = get_object_or_404(
                    Container,
                    archival_unit__fonds=int(fonds),
                    archival_unit__subfonds=int(subfonds),
                    archival_unit__series=int(series),
                    container_no=int(container_no)
                )
                return container

        raise NotFound(detail="Error 404, page not found", code=404)

