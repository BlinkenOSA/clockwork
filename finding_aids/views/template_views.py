from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from extra_views import NamedFormsetsMixin, CreateWithInlinesView, UpdateWithInlinesView
from fm.views import AjaxDeleteView

from archival_unit.models import ArchivalUnit
from clockwork.mixins import InlineSuccessMessageMixin, AuditTrailContextMixin
from finding_aids.forms import FindingAidsAssociatedPeopleInline, \
    FindingAidsAssociatedCorporationInline, FindingAidsAssociatedCountryInline, FindingAidsAssociatedPlaceInline, \
    FindingAidsLanguageInline, FindingAidsExtentInline, FindingAidsTemplateForm, FindingAidsDateInline
from finding_aids.mixins import FindingAidsPermissionMixin, FindingAidsTemplateAllowedArchivalUnitMixin
from finding_aids.models import FindingAidsEntity


class FindingAidsTemplateList(FindingAidsPermissionMixin, FindingAidsTemplateAllowedArchivalUnitMixin, TemplateView):
    template_name = 'finding_aids/template_view/list.html'

    def get_context_data(self, **kwargs):
        context = super(FindingAidsTemplateList, self).get_context_data(**kwargs)
        context['series'] = ArchivalUnit.objects.get(pk=kwargs['series_id'])
        return context


class FindingAidsTemplateListJson(FindingAidsPermissionMixin, BaseDatatableView):
    model = FindingAidsEntity
    columns = ['level', 'template_name', 'user_created', 'action']
    order_columns = ['folder_no', 'sequence_no', 'template_name']
    max_display_length = 500

    def get_initial_queryset(self):
        archival_unit = ArchivalUnit.objects.get(pk=self.kwargs['series_id'])
        finding_aids_entities = FindingAidsEntity.objects.filter(archival_unit=archival_unit,
                                                                 is_template=True).order_by('template_name')
        return finding_aids_entities

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('finding_aids/template_view/table_action_buttons.html', context={
                'series_id': row.archival_unit.id, 'id': row.id})
        else:
            return super(FindingAidsTemplateListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class FindingAidsTemplateCreate(FindingAidsPermissionMixin, FindingAidsTemplateAllowedArchivalUnitMixin,
                                InlineSuccessMessageMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = FindingAidsEntity
    form_class = FindingAidsTemplateForm
    template_name = 'finding_aids/template_view/form.html'
    success_message = "%(template_name)s was created successfully"
    inlines = [FindingAidsAssociatedPeopleInline, FindingAidsAssociatedCorporationInline,
               FindingAidsAssociatedCountryInline, FindingAidsAssociatedPlaceInline, FindingAidsLanguageInline,
               FindingAidsExtentInline, FindingAidsDateInline]
    inlines_names = ['associated_people', 'associated_corporations', 'associated_countries', 'associated_places',
                     'languages', 'extents', 'dates']

    def get_success_url(self):
        return reverse_lazy('finding_aids:finding_aids_template_list',
                            kwargs={'series_id': self.kwargs['series_id']})

    def get_initial(self):
        initial = {}
        archival_unit = ArchivalUnit.objects.get(pk=self.kwargs['series_id'])
        initial['level'] = 'F'
        initial['folder_no'] = 0
        initial['archival_reference_code'] = "%s/0:0" % archival_unit.reference_code
        return initial

    def get_context_data(self, **kwargs):
        context = super(FindingAidsTemplateCreate, self).get_context_data(**kwargs)
        context['series'] = ArchivalUnit.objects.get(pk=self.kwargs['series_id'])
        return context

    def forms_valid(self, form, formset):
        archival_unit = ArchivalUnit.objects.get(pk=self.kwargs['series_id'])
        self.object.archival_unit = archival_unit
        self.object.is_template = True
        return super(FindingAidsTemplateCreate, self).forms_valid(form, formset)


class FindingAidsTemplateUpdate(FindingAidsPermissionMixin, AuditTrailContextMixin,
                                FindingAidsTemplateAllowedArchivalUnitMixin, InlineSuccessMessageMixin,
                                NamedFormsetsMixin, UpdateWithInlinesView):
    model = FindingAidsEntity
    form_class = FindingAidsTemplateForm
    template_name = 'finding_aids/template_view/form.html'
    success_message = "%(template_name)s was updated successfully"
    inlines = [FindingAidsAssociatedPeopleInline, FindingAidsAssociatedCorporationInline,
               FindingAidsAssociatedCountryInline, FindingAidsAssociatedPlaceInline, FindingAidsLanguageInline,
               FindingAidsExtentInline, FindingAidsDateInline]
    inlines_names = ['associated_people', 'associated_corporations', 'associated_countries', 'associated_places',
                     'languages', 'extents', 'dates']

    def get_success_url(self):
        return reverse_lazy('finding_aids:finding_aids_template_list',
                            kwargs={'series_id': self.kwargs['series_id']})

    def get_context_data(self, **kwargs):
        context = super(FindingAidsTemplateUpdate, self).get_context_data(**kwargs)
        context['series'] = ArchivalUnit.objects.get(pk=self.kwargs['series_id'])
        return context

    def forms_valid(self, form, formset):
        archival_unit = ArchivalUnit.objects.get(pk=self.kwargs['series_id'])
        self.object.archival_unit = archival_unit
        self.object.is_template = True
        return super(FindingAidsTemplateUpdate, self).forms_valid(form, formset)


class FindingAidsTemplateDelete(FindingAidsPermissionMixin, FindingAidsTemplateAllowedArchivalUnitMixin,
                                AjaxDeleteView):
    model = FindingAidsEntity
    template_name = 'finding_aids/template_view/delete.html'
    context_object_name = 'finding_aids'
    success_message = ugettext("Finding Aids record was deleted successfully!")

    def get_success_result(self):
        msg = ugettext("Finding Aids Template: %s was deleted successfully!") % self.object.template_name
        return {'status': 'ok', 'message': msg}
