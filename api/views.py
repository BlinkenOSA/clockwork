# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404

from api.permission import APIGroupPermission
from api.serializers import ContainerDigitizedSerializer
from container.models import Container


class GetSetDigitizedContainer(RetrieveUpdateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerDigitizedSerializer
    lookup_field = 'barcode'
    permission_classes = (APIGroupPermission, )