from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from authority.forms import CountryForm
from authority.models import Country
from clockwork.ajax_extra_views import AjaxDeleteProtectedView
from donor.models import Donor
from finding_aids.models import FindingAidsEntityAssociatedCountry


class CountryList(TemplateView):
    template_name = 'authority/country/list.html'


class CountryListJson(BaseDatatableView):
    model = Country
    columns = ['id', 'country', 'authority_url', 'alpha2', 'alpha3', 'action']
    order_columns = ['country', 'alpha2', 'alpha3']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(country__icontains=search) |
                Q(alpha2__icontains=search) |
                Q(alpha3__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            fa_exists = FindingAidsEntityAssociatedCountry.objects.filter(associated_country=row).exists()
            donor_exists = Donor.objects.filter(country=row).exists()
            exists = fa_exists or donor_exists
            return render_to_string('authority/country/table_action_buttons.html',
                                    context={'id': row.id, 'exists': exists})
        elif column == 'authority_url':
            return '<a href="%s" target="_blank">%s</a>' % (row.authority_url, row.authority_url) \
                if row.authority_url else None
        else:
            return super(CountryListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class CountryCreate(AjaxCreateView):
    form_class = CountryForm
    model = Country
    template_name = 'authority/country/form.html'

    def get_response_message(self):
        return ugettext("Country: %s was created successfully!") % self.object.country


class CountryUpdate(AjaxUpdateView):
    form_class = CountryForm
    model = Country
    template_name = 'authority/country/form.html'

    def get_response_message(self):
        return ugettext("Country: %s was updated successfully!") % self.object.country


class CountryDelete(AjaxDeleteProtectedView):
    model = Country
    template_name = 'authority/country/delete.html'
    context_object_name = 'country'
    success_message = ugettext("Country was deleted successfully!")
    error_message = ugettext("Country can't be deleted, because it has already been assigned to an entry!")
