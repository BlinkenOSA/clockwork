
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from controlled_list.forms import RightsRestrictionReasonForm
from controlled_list.models import RightsRestrictionReason


class RightsRestrictionReasonList(TemplateView):
    template_name = 'controlled_list/rights_restriction_reason/list.html'


class RightsRestrictionReasonListJson(BaseDatatableView):
    model = RightsRestrictionReason
    columns = ['id', 'reason', 'action']
    order_columns = ['reason']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(reason__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('controlled_list/rights_restriction_reason/table_action_buttons.html', context={'id': row.id})
        else:
            return super(RightsRestrictionReasonListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class RightsRestrictionReasonCreate(AjaxCreateView):
    form_class = RightsRestrictionReasonForm
    model = RightsRestrictionReason
    template_name = 'controlled_list/rights_restriction_reason/form.html'

    def get_response_message(self):
        return ugettext("RightsRestrictionReason: %s was created successfully!") % self.object


class RightsRestrictionReasonUpdate(AjaxUpdateView):
    form_class = RightsRestrictionReasonForm
    model = RightsRestrictionReason
    template_name = 'controlled_list/rights_restriction_reason/form.html'

    def get_response_message(self):
        return ugettext("RightsRestrictionReason: %s was updated successfully!") % self.object