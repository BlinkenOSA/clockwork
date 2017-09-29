from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from clockwork.mixins import GeneralAllPermissionMixin
from controlled_list.forms import LanguageUsageForm
from controlled_list.models import LanguageUsage


class LanguageUsagePermissionMixin(GeneralAllPermissionMixin):
    permission_model = LanguageUsage


class LanguageUsageList(LanguageUsagePermissionMixin, TemplateView):
    template_name = 'controlled_list/language_usage/list.html'


class LanguageUsageListJson(LanguageUsagePermissionMixin, BaseDatatableView):
    model = LanguageUsage
    columns = ['id', 'usage', 'action']
    order_columns = ['usage']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(usage__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('controlled_list/language_usage/table_action_buttons.html', context={'id': row.id})
        else:
            return super(LanguageUsageListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class LanguageUsageCreate(LanguageUsagePermissionMixin, AjaxCreateView):
    form_class = LanguageUsageForm
    model = LanguageUsage
    template_name = 'controlled_list/language_usage/form.html'

    def get_response_message(self):
        return ugettext("LanguageUsage: %s was created successfully!") % self.object.usage


class LanguageUsageUpdate(LanguageUsagePermissionMixin, AjaxUpdateView):
    form_class = LanguageUsageForm
    model = LanguageUsage
    template_name = 'controlled_list/language_usage/form.html'

    def get_response_message(self):
        return ugettext("LanguageUsage: %s was updated successfully!") % self.object.usage
