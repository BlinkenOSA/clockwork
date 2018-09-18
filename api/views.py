# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView

from api.permission import APIGroupPermission
from api.serializers.container_serializers import ContainerDigitizedSerializer
from api.serializers.finding_aids_serializer import FindingAidsSerializer
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