from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext
from django.views.generic import TemplateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from authority.forms import GenreForm
from authority.models import Genre


class GenreList(TemplateView):
    template_name = 'authority/genre/list.html'


class GenreListJson(BaseDatatableView):
    model = Genre
    columns = ['id', 'genre', 'authority_url', 'action']
    order_columns = ['genre']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(genre__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('authority/genre/table_action_buttons.html', context={'id': row.id})
        elif column == 'authority_url':
            return '<a href="%s" target="_blank">%s</a>' % (row.authority_url, row.authority_url) \
                if row.authority_url else None
        else:
            return super(GenreListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class GenreCreate(AjaxCreateView):
    form_class = GenreForm
    model = Genre
    template_name = 'authority/genre/form.html'

    def get_response_message(self):
        return ugettext("Genre: %s was created successfully!") % self.object


class GenreUpdate(AjaxUpdateView):
    form_class = GenreForm
    model = Genre
    template_name = 'authority/genre/form.html'

    def get_response_message(self):
        return ugettext("Genre: %s was updated successfully!") % self.object


class GenreDelete(DeleteView):
    model = Genre
    template_name = 'authority/genre/delete.html'
    context_object_name = 'genre'
    success_url = reverse_lazy('authority:genre_list')
    success_message = ugettext("Genre was deleted successfully")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(GenreDelete, self).delete(request, *args, **kwargs)

