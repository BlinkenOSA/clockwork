from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from authority.forms import LanguageForm
from authority.models import Language


class LanguageList(TemplateView):
    template_name = 'authority/language/list.html'


class LanguageListJson(BaseDatatableView):
    model = Language
    columns = ['id', 'language', 'iso_639_1', 'iso_639_2', 'action']
    order_columns = ['language', 'iso_639_1', 'iso_639_2']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(language__icontains=search) |
                Q(iso_639_1__icontains=search) |
                Q(iso_639_1__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('authority/language/table_action_buttons.html', context={'id': row.id})
        else:
            return super(LanguageListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class LanguageCreate(AjaxCreateView):
    form_class = LanguageForm
    model = Language
    template_name = 'authority/language/form.html'

    def get_response_message(self):
        return ugettext("Language: %s was created successfully!") % self.object.language


class LanguageUpdate(AjaxUpdateView):
    form_class = LanguageForm
    model = Language
    template_name = 'authority/language/form.html'

    def get_response_message(self):
        return ugettext("Language: %s was updated successfully!") % self.object.language


class LanguageDelete(DeleteView):
    model = Language
    template_name = 'authority/language/delete.html'
    context_object_name = 'language'
    success_url = reverse_lazy('authority:language_list')
    success_message = ugettext("Language was deleted successfully")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(LanguageDelete, self).delete(request, *args, **kwargs)


class LanguagePopupCreate(SuccessMessageMixin, AjaxCreateView):
    model = Language
    template_name = 'authority/language/form_popup.html'

    def get_success_result(self):
        return {
            'status': 'ok',
            'message': self.get_response_message(),
            'entry_id': self.object.id,
            'entry_name': self.object.name
        }