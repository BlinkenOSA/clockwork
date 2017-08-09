from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext
from django.views.generic import TemplateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from extra_views import NamedFormsetsMixin
from fm.views import AjaxCreateView, AjaxUpdateView

from authority.forms import PersonForm, PersonOtherNamesInLine
from authority.models import Person
from clockwork.inlineform import CreateWithInlinesAjaxView, UpdateWithInlinesAjaxView


class PersonList(TemplateView):
    template_name = 'authority/person/list.html'


class PersonListJson(BaseDatatableView):
    model = Person
    columns = ['id', 'person_name', 'action']
    order_columns = ['last_name', 'first_name']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('authority/person/table_action_buttons.html', context={'id': row.id})
        elif column == 'person_name':
            return ', '.join([row.last_name, row.first_name])
        else:
            return super(PersonListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class PersonCreate(NamedFormsetsMixin, CreateWithInlinesAjaxView):
    form_class = PersonForm
    model = Person
    template_name = 'authority/person/form.html'
    inlines = [PersonOtherNamesInLine]
    inlines_names = ['people_other_names']

    def get_response_message(self):
        return ugettext("Person: %s was created successfully!") % self.object


class PersonUpdate(NamedFormsetsMixin, UpdateWithInlinesAjaxView):
    form_class = PersonForm
    model = Person
    template_name = 'authority/person/form.html'
    inlines = [PersonOtherNamesInLine]
    inlines_names = ['people_other_names']

    def get_response_message(self):
        return ugettext("Person: %s was updated successfully!") % self.object


class PersonDelete(DeleteView):
    model = Person
    template_name = 'authority/person/delete.html'
    context_object_name = 'person'
    success_url = reverse_lazy('authority:person_list')
    success_message = ugettext("Person was deleted successfully")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PersonDelete, self).delete(request, *args, **kwargs)


class PersonPopupCreate(SuccessMessageMixin, AjaxCreateView):
    model = Person
    template_name = 'authority/person/form_popup.html'

    def get_success_result(self):
        return {
            'status': 'ok',
            'message': self.get_response_message(),
            'entry_id': self.object.id,
            'entry_name': self.object.name
        }