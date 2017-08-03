from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import DetailView, DeleteView, TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from extra_views import CreateWithInlinesView, NamedFormsetsMixin, UpdateWithInlinesView

from clockwork.mixins import InlineSuccessMessageMixin
from isaar.forms import IsaarForm, OtherNamesInline, StandardizedNamesInline, CorporateBodyIdentifiersInLine, \
    PlacesInline, TYPE_CHOICES
from isaar.models import Isaar


class IsaarList(TemplateView):
    template_name = 'isaar/list.html'


class IsaarListJson(BaseDatatableView):
    model = Isaar
    columns = ['id', 'name', 'type', 'status', 'action']
    order_columns = ['id', 'name', '', '', '']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(type__country__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('isaar/table_action_buttons.html', context={'id': row.id})
        elif column == 'type':
            return dict(TYPE_CHOICES)[row.type]
        else:
            return super(IsaarListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class IsaarDetail(DetailView):
    model = Isaar
    template_name = 'isaar/detail.html'
    context_object_name = 'isaar'

    def get_context_data(self, **kwargs):
        context = super(IsaarDetail, self).get_context_data(**kwargs)
        context['type'] = dict(TYPE_CHOICES)[self.object.type]
        return context


class IsaarCreate(InlineSuccessMessageMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Isaar
    form_class = IsaarForm
    template_name = 'isaar/form.html'
    success_url = reverse_lazy('isaar:list')
    success_message = ugettext("%(name)s was created successfully")
    inlines = [OtherNamesInline, StandardizedNamesInline, CorporateBodyIdentifiersInLine, PlacesInline]
    inlines_names = ['other_names', 'standardized_names', 'corporate_body_identifiers', 'places']


class IsaarUpdate(InlineSuccessMessageMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = Isaar
    form_class = IsaarForm
    template_name = 'isaar/form.html'
    success_url = reverse_lazy('isaar:list')
    success_message = ugettext("%(name)s was updated successfully")
    inlines = [OtherNamesInline, StandardizedNamesInline, CorporateBodyIdentifiersInLine, PlacesInline]
    inlines_names = ['other_names', 'standardized_names', 'corporate_body_identifiers', 'places']


class IsaarDelete(DeleteView):
    model = Isaar
    template_name = 'isaar/delete.html'
    context_object_name = 'isaar'
    success_url = reverse_lazy('isaar:list')
    success_message = ugettext("ISAAR/CPF record was deleted successfully")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(IsaarDelete, self).delete(request, *args, **kwargs)