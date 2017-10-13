from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from clockwork.mixins import GeneralAllPermissionMixin
from controlled_list.forms import ArchivalUnitThemeForm
from controlled_list.models import ArchivalUnitTheme


class ArchivalUnitThemeMixin(GeneralAllPermissionMixin):
    permission_model = ArchivalUnitTheme


class ArchivalUnitThemeList(ArchivalUnitThemeMixin, TemplateView):
    template_name = 'controlled_list/archival_unit_theme/list.html'


class ArchivalUnitThemeListJson(ArchivalUnitThemeMixin, BaseDatatableView):
    model = ArchivalUnitTheme
    columns = ['id', 'theme', 'action']
    order_columns = ['theme']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(theme__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('controlled_list/archival_unit_theme/table_action_buttons.html', context={'id': row.id})
        else:
            return super(ArchivalUnitThemeListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class ArchivalUnitThemeCreate(ArchivalUnitThemeMixin, AjaxCreateView):
    form_class = ArchivalUnitThemeForm
    model = ArchivalUnitTheme
    template_name = 'controlled_list/archival_unit_theme/form.html'

    def get_response_message(self):
        return ugettext("Archival Unit Theme: %s was created successfully!") % self.object


class ArchivalUnitThemeUpdate(ArchivalUnitThemeMixin, AjaxUpdateView):
    form_class = ArchivalUnitThemeForm
    model = ArchivalUnitTheme
    template_name = 'controlled_list/archival_unit_theme/form.html'

    def get_response_message(self):
        return ugettext("Archival Unit Theme: %s was updated successfully!") % self.object
