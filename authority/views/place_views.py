from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext
from django.views.generic import TemplateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from authority.forms import PlaceForm
from authority.models import Place


class PlaceList(TemplateView):
    template_name = 'authority/place/list.html'


class PlaceListJson(BaseDatatableView):
    model = Place
    columns = ['id', 'place', 'wiki_url', 'authority_url', 'action']
    order_columns = ['place']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(place__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('authority/place/table_action_buttons.html', context={'id': row.id})
        else:
            return super(PlaceListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class PlaceCreate(AjaxCreateView):
    form_class = PlaceForm
    model = Place
    template_name = 'authority/place/form.html'

    def get_response_message(self):
        return ugettext("Place: %s was created successfully!") % self.object


class PlaceUpdate(AjaxUpdateView):
    form_class = PlaceForm
    model = Place
    template_name = 'authority/place/form.html'

    def get_response_message(self):
        return ugettext("Place: %s was updated successfully!") % self.object


class PlaceDelete(DeleteView):
    model = Place
    template_name = 'authority/place/delete.html'
    context_object_name = 'place'
    success_url = reverse_lazy('authority:place_list')
    success_message = ugettext("Place was deleted successfully")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PlaceDelete, self).delete(request, *args, **kwargs)


class PlacePopupCreate(SuccessMessageMixin, AjaxCreateView):
    model = Place
    template_name = 'authority/place/form_popup.html'

    def get_success_result(self):
        return {
            'status': 'ok',
            'message': self.get_response_message(),
            'entry_id': self.object.id,
            'entry_name': self.object.name
        }