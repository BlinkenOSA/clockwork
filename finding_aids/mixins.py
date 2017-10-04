from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from archival_unit.models import ArchivalUnit
from clockwork.mixins import GeneralAllPermissionMixin
from container.models import Container
from finding_aids.models import FindingAidsEntity


class FindingAidsPermissionMixin(GeneralAllPermissionMixin):
    permission_model = FindingAidsEntity


class FindingAidsTemplateAllowedArchivalUnitMixin(object):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user.user_profile.allowed_archival_units.count():
            archival_unit = get_object_or_404(ArchivalUnit, pk=self.kwargs['series_id'])

            if archival_unit in user.user_profile.allowed_archival_units.all():
                return super(FindingAidsTemplateAllowedArchivalUnitMixin, self).get(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            return super(FindingAidsTemplateAllowedArchivalUnitMixin, self).get(request, *args, **kwargs)


class FindingAidsAllowedArchivalUnitMixin(object):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user.user_profile.allowed_archival_units.count():
            container = get_object_or_404(Container, pk=self.kwargs['container_id'])
            archival_unit = container.archival_unit

            if archival_unit in user.user_profile.allowed_archival_units.all():
                return super(FindingAidsAllowedArchivalUnitMixin, self).get(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            return super(FindingAidsAllowedArchivalUnitMixin, self).get(request, *args, **kwargs)