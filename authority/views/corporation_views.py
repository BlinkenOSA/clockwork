from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from extra_views import NamedFormsetsMixin

from authority.forms import CorporationForm, CorporationOtherNamesInLine
from authority.models import Corporation
from clockwork.ajax_extra_views import AjaxDeleteProtectedView
from clockwork.inlineform import CreateWithInlinesAjaxView, UpdateWithInlinesAjaxView
from finding_aids.models import FindingAidsEntityAssociatedCorporation


class CorporationList(TemplateView):
    template_name = 'authority/corporation/list.html'


class CorporationListJson(BaseDatatableView):
    model = Corporation
    columns = ['id', 'name', 'authority_url', 'action']
    order_columns = ['name', '']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            exists = FindingAidsEntityAssociatedCorporation.objects.filter(associated_corporation=row).exists()
            return render_to_string('authority/corporation/table_action_buttons.html',
                                    context={'id': row.id, 'exists': exists})
        elif column == 'authority_url':
            return '<a href="%s" target="_blank">%s</a>' % (row.authority_url, row.authority_url) \
                if row.authority_url else None
        else:
            return super(CorporationListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class CorporationCreate(NamedFormsetsMixin, CreateWithInlinesAjaxView):
    form_class = CorporationForm
    model = Corporation
    template_name = 'authority/corporation/form.html'
    inlines = [CorporationOtherNamesInLine]
    inlines_names = ['corporation_other_names']

    def get_response_message(self):
        return ugettext("Corporation: %s was created successfully!") % self.object.name

    def get_success_result(self):
        results = super(CorporationCreate, self).get_success_result()
        results['entry_id'] = self.object.id,
        results['entry_name'] = self.object.name
        return results


class CorporationUpdate(NamedFormsetsMixin, UpdateWithInlinesAjaxView):
    form_class = CorporationForm
    model = Corporation
    template_name = 'authority/corporation/form.html'
    inlines = [CorporationOtherNamesInLine]
    inlines_names = ['corporation_other_names']

    def get_response_message(self):
        return ugettext("Corporation: %s was updated successfully!") % self.object.name


class CorporationDelete(AjaxDeleteProtectedView):
    model = Corporation
    template_name = 'authority/corporation/delete.html'
    context_object_name = 'corporation'
    success_message = ugettext("Corporation was deleted successfully!")
    error_message = ugettext("Corporation can't be deleted, because it has already been assigned to an entry!")

