from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView

from authority.forms import PlaceForm
from authority.models import Place
from clockwork.mixins import GeneralAllPermissionMixin
from finding_aids.models import FindingAidsEntityAssociatedPlace


class AccessionPermissionMixin(GeneralAllPermissionMixin):
    permission_model = Place


class PlaceList(AccessionPermissionMixin, TemplateView):
    template_name = 'authority/place/list.html'


class PlaceListJson(AccessionPermissionMixin, BaseDatatableView):
    model = Place
    columns = ['id', 'place', 'authority_url', 'action']
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
            exists = FindingAidsEntityAssociatedPlace.objects.filter(associated_place=row).exists()
            return render_to_string('authority/place/table_action_buttons.html',
                                    context={'id': row.id, 'exists': exists})
        elif column == 'authority_url':
            return '<a href="%s" target="_blank">%s</a>' % (row.authority_url, row.authority_url) \
                if row.authority_url else None
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


class PlaceCreate(AccessionPermissionMixin, AjaxCreateView):
    form_class = PlaceForm
    model = Place
    template_name = 'authority/place/form.html'

    def get_response_message(self):
        return ugettext("Place: %s was created successfully!") % self.object

    def get_success_result(self):
        results = super(PlaceCreate, self).get_success_result()
        results['entry_id'] = self.object.id,
        results['entry_name'] = self.object.place
        return results


class PlaceUpdate(AccessionPermissionMixin, AjaxUpdateView):
    form_class = PlaceForm
    model = Place
    template_name = 'authority/place/form.html'

    def get_response_message(self):
        return ugettext("Place: %s was updated successfully!") % self.object


class PlaceDelete(AccessionPermissionMixin, AjaxDeleteView):
    model = Place
    template_name = 'authority/place/delete.html'
    context_object_name = 'place'
    success_message = ugettext("Place was deleted successfully!")
    error_message = ugettext("Place can't be deleted, because it has already been assigned to an entry!")