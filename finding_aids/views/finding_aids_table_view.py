from django.db.models import Count
from django.views.generic import TemplateView

from archival_unit.models import ArchivalUnit
from controlled_list.models import CarrierType
from finding_aids.mixins import FindingAidsPermissionMixin, FindingAidsAllowedArchivalUnitMixin


class FindingAidsTableViewList(FindingAidsPermissionMixin, FindingAidsAllowedArchivalUnitMixin, TemplateView):
    template_name = 'finding_aids/table_view/list.html'

    def get_context_data(self, **kwargs):
        context = super(FindingAidsTableViewList, self).get_context_data(**kwargs)
        archival_unit = ArchivalUnit.objects.get(pk=kwargs['series_id'])
        context['series'] = archival_unit
        return context
