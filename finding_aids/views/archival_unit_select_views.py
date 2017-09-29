from django.views.generic import FormView
from finding_aids.forms import FindingAidsArchivalUnitForm
from finding_aids.mixins import FindingAidsPermissionMixin


class FindingAidsArchivalUnit(FindingAidsPermissionMixin, FormView):
    template_name = 'finding_aids/select_archival_unit/select_archival_unit.html'
    form_class = FindingAidsArchivalUnitForm
