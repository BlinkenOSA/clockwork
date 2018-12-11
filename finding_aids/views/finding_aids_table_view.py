from django.views.generic import TemplateView

from archival_unit.models import ArchivalUnit
from finding_aids.mixins import FindingAidsPermissionMixin, FindingAidsAllowedArchivalUnitMixin


class FindingAidsTableViewList(FindingAidsPermissionMixin, FindingAidsAllowedArchivalUnitMixin, TemplateView):
    template_name = 'finding_aids/table_view/list.html'

    def get_context_data(self, **kwargs):
        context = super(FindingAidsTableViewList, self).get_context_data(**kwargs)
        context['series'] = ArchivalUnit.objects.get(pk=kwargs['series_id'])
        return context
