from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from authority.forms import CountryForm
from authority.models import Country


class CountryList(TemplateView):
    template_name = 'authority/country/list.html'


class CountryListJson(BaseDatatableView):
    model = Country
    columns = ['id', 'country', 'alpha2', 'alpha3', 'action']
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
            return render_to_string('authority/country/table_action_buttons.html', context={'id': row.id})
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


class CountryDelete(DeleteView):
    model = Country
    template_name = 'authority/country/delete.html'
    context_object_name = 'country'
    success_url = reverse_lazy('authority:country_list')
    success_message = ugettext("Country was deleted successfully")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CountryDelete, self).delete(request, *args, **kwargs)


class CountryPopupCreate(SuccessMessageMixin, AjaxCreateView):
    model = Country
    template_name = 'authority/country/form_popup.html'

    def get_success_result(self):
        return {
            'status': 'ok',
            'message': self.get_response_message(),
            'entry_id': self.object.id,
            'entry_name': self.object.name
        }