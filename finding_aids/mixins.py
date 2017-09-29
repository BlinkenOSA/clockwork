from clockwork.mixins import GeneralAllPermissionMixin
from finding_aids.models import FindingAidsEntity


class FindingAidsPermissionMixin(GeneralAllPermissionMixin):
    permission_model = FindingAidsEntity
