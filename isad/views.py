from braces.views import JSONResponseMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import FormView, DeleteView, DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView
from extra_views import NamedFormsetsMixin, CreateWithInlinesView, UpdateWithInlinesView
from fm.views import AjaxDeleteView

from archival_unit.models import ArchivalUnit
from clockwork.mixins import InlineSuccessMessageMixin
from isad.forms import IsadArchivalUnitForm, IsadForm, IsadCreatorInline, IsadExtentInline, IsadCarrierInline, \
    IsadRelatedFindingAidsInline, IsadLocationOfOriginalsInline, IsadLocationOfCopiesInline
from isad.models import Isad


class IsadList(FormView):
    template_name = 'isad/list.html'
    form_class = IsadArchivalUnitForm


class IsadListJson(BaseDatatableView):
    model = Isad
    columns = ['reference_code', 'title', 'view-edit-delete', 'action']
    order_columns = ['reference_code', 'title', '', '']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(reference_code__icontains=search) |
                Q(title__country__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('isad/table_publish_buttons.html', context={'isad': row})
        elif column == 'view-edit-delete':
            return render_to_string('isad/table_action_buttons.html', context={'id': row.id})
        else:
            return super(IsadListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class IsadDetail(DetailView):
    model = Isad
    template_name = 'isad/detail.html'
    context_object_name = 'isad'


class IsadCreate(InlineSuccessMessageMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Isad
    form_class = IsadForm
    template_name = 'isad/form.html'
    success_url = reverse_lazy('isad:list')
    success_message = ugettext("ISAD(G) Record: %(reference_code)s was created successfully!")
    inlines = [IsadCreatorInline, IsadExtentInline, IsadCarrierInline, IsadRelatedFindingAidsInline,
               IsadLocationOfOriginalsInline, IsadLocationOfCopiesInline]
    inlines_names = ['creators', 'extents', 'carriers', 'related_finding_aids', 'location_of_originals',
                     'location_of_copies']

    def get_initial(self):
        initial = {}
        archival_unit = ArchivalUnit.objects.get(pk=self.kwargs['archival_unit'])
        initial['archival_unit'] = archival_unit
        initial['reference_code'] = archival_unit.reference_code
        initial['description_level'] = archival_unit.level
        initial['title'] = archival_unit.title
        initial['level'] = archival_unit.level
        return initial


class IsadUpdate(InlineSuccessMessageMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = Isad
    form_class = IsadForm
    template_name = 'isad/form.html'
    success_url = reverse_lazy('isad:list')
    success_message = ugettext("ISAD(G) Record: %(reference_code)s was updated successfully!")
    inlines = [IsadCreatorInline, IsadExtentInline, IsadCarrierInline, IsadRelatedFindingAidsInline,
               IsadLocationOfOriginalsInline, IsadLocationOfCopiesInline]
    inlines_names = ['creators', 'extents', 'carriers', 'related_finding_aids', 'location_of_originals',
                     'location_of_copies']


class IsadDelete(AjaxDeleteView):
    model = Isad
    template_name = 'isad/delete.html'
    context_object_name = 'isad'

    def get_success_result(self):
        msg = ugettext("ISAD(G) Record: %s was deleted successfully!") % self.object.reference_code
        return {'status': 'ok', 'message': msg}


class IsadAction(JSONResponseMixin, DetailView):
    model = Isad

    def post(self, request, *args, **kwargs):
        action = self.kwargs['action']
        isad = self.get_object()

        if action == 'publish':
            isad.published = True

        if action == 'unpublish':
            isad.published = False

        isad.save()

        context = {
            'DT_rowId': isad.id,
            'title': isad.title,
            'reference_code': isad.reference_code,
            'action': render_to_string('isad/table_publish_buttons.html', context={'isad': isad}),
            'view-edit-delete': render_to_string('isad/table_action_buttons.html', context={'id': isad.id})
        }
        return self.render_json_response(context)
