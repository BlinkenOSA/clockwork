from braces.views import JSONResponseMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import FormView, DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView
from extra_views import NamedFormsetsMixin, CreateWithInlinesView, UpdateWithInlinesView
from fm.views import AjaxDeleteView
from django.core.exceptions import PermissionDenied

from archival_unit.models import ArchivalUnit
from clockwork.mixins import InlineSuccessMessageMixin, GeneralAllPermissionMixin, AuditTrailContextMixin
from isad.forms import IsadArchivalUnitForm, IsadForm, IsadCreatorInline, IsadExtentInline, IsadCarrierInline, \
    IsadRelatedFindingAidsInline, IsadLocationOfOriginalsInline, IsadLocationOfCopiesInline
from isad.models import Isad


class IsadPermissionMixin(GeneralAllPermissionMixin):
    permission_model = Isad


class IsadAllowedArchivalUnitMixin(object):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user.user_profile.allowed_archival_units.count():
            if 'archival_unit' in self.kwargs:
                archival_unit = get_object_or_404(ArchivalUnit, pk=self.kwargs['archival_unit'])
            else:
                archival_unit = get_object_or_404(ArchivalUnit, pk=self.kwargs['pk'])

            if archival_unit in user.user_profile.allowed_archival_units.all():
                return super(IsadAllowedArchivalUnitMixin, self).get(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            return super(IsadAllowedArchivalUnitMixin, self).get(request, *args, **kwargs)


class IsadList(IsadPermissionMixin, FormView):
    template_name = 'isad/list.html'

    def get_form(self, form_class=None):
        return IsadArchivalUnitForm(user=self.request.user)


class IsadListJson(IsadPermissionMixin, BaseDatatableView):
    model = Isad
    columns = ['reference_code', 'title', 'view-edit-delete', 'action']
    order_columns = ['reference_code', 'title', '', '']
    max_display_length = 500

    def get_initial_queryset(self):
        user = self.request.user
        if len(user.user_profile.allowed_archival_units.all()) > 0:
            return Isad.objects.filter(archival_unit__in=user.user_profile.allowed_archival_units.all())
        else:
            return Isad.objects.all()

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


class IsadCreate(IsadPermissionMixin, IsadAllowedArchivalUnitMixin, InlineSuccessMessageMixin,
                 NamedFormsetsMixin, CreateWithInlinesView):
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
        initial['reference_code'] = archival_unit.reference_code
        initial['description_level'] = archival_unit.level
        initial['title'] = archival_unit.title
        initial['level'] = archival_unit.level
        return initial

    def forms_valid(self, form, formset):
        archival_unit = ArchivalUnit.objects.get(pk=self.kwargs['archival_unit'])
        self.object.archival_unit = archival_unit
        return super(IsadCreate, self).forms_valid(form, formset)


class IsadUpdate(IsadPermissionMixin, AuditTrailContextMixin, IsadAllowedArchivalUnitMixin, InlineSuccessMessageMixin,
                 NamedFormsetsMixin, UpdateWithInlinesView):
    model = Isad
    form_class = IsadForm
    template_name = 'isad/form.html'
    success_url = reverse_lazy('isad:list')
    success_message = ugettext("ISAD(G) Record: %(reference_code)s was updated successfully!")
    inlines = [IsadCreatorInline, IsadExtentInline, IsadCarrierInline, IsadRelatedFindingAidsInline,
               IsadLocationOfOriginalsInline, IsadLocationOfCopiesInline]
    inlines_names = ['creators', 'extents', 'carriers', 'related_finding_aids', 'location_of_originals',
                     'location_of_copies']


class IsadDelete(IsadPermissionMixin, IsadAllowedArchivalUnitMixin, AjaxDeleteView):
    model = Isad
    template_name = 'isad/delete.html'
    context_object_name = 'isad'

    def get_success_result(self):
        msg = ugettext("ISAD(G) Record: %s was deleted successfully!") % self.object.reference_code
        return {'status': 'ok', 'message': msg}


class IsadAction(IsadPermissionMixin, IsadAllowedArchivalUnitMixin, JSONResponseMixin, DetailView):
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
