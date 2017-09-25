from django.views.generic import FormView
from finding_aids.forms import FindingAidsArchivalUnitForm


class FindingAidsArchivalUnit(FormView):
    template_name = 'finding_aids/select_archival_unit/select_archival_unit.html'
    form_class = FindingAidsArchivalUnitForm
