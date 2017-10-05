from django.db.models import AutoField, UUIDField, ForeignKey
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from extra_views import NamedFormsetsMixin, CreateWithInlinesView, UpdateWithInlinesView
from fm.views import JSONResponseMixin, AjaxDeleteView

from clockwork.mixins import InlineSuccessMessageMixin, AuditTrailContextMixin
from finding_aids.forms import *
from finding_aids.mixins import FindingAidsPermissionMixin, FindingAidsAllowedArchivalUnitMixin
from finding_aids.views.helper_functions import *


class FindingAidsCreate(FindingAidsPermissionMixin, FindingAidsAllowedArchivalUnitMixin, InlineSuccessMessageMixin,
                        NamedFormsetsMixin, CreateWithInlinesView):
    model = FindingAidsEntity
    form_class = FindingAidsForm
    template_name = 'finding_aids/container_view/form.html'
    success_message = "%(title)s was created successfully"
    inlines = [FindingAidsAssociatedPeopleInline, FindingAidsAssociatedCorporationInline,
               FindingAidsAssociatedCountryInline, FindingAidsAssociatedPlaceInline, FindingAidsLanguageInline,
               FindingAidsExtentInline]
    inlines_names = ['associated_people', 'associated_corporations', 'associated_countries', 'associated_places',
                     'languages', 'extents']

    def get_success_url(self):
        return reverse_lazy('finding_aids:finding_aids_container_list',
                            kwargs={'container_id': self.kwargs['container_id']})

    def get_initial(self):
        initial = {}
        container = Container.objects.get(pk=self.kwargs['container_id'])
        initial['level'] = 'F'
        folder_no = get_number_of_folders(container.id) + 1
        initial['folder_no'] = folder_no
        initial['archival_reference_code'] = "%s/%s:%s" % (container.archival_unit.reference_code,
                                                           container.container_no, folder_no)
        return initial

    def get_context_data(self, **kwargs):
        context = super(FindingAidsCreate, self).get_context_data(**kwargs)
        context['container'] = Container.objects.get(pk=self.kwargs['container_id'])
        return context

    def forms_valid(self, form, formset):
        container = Container.objects.get(pk=self.kwargs['container_id'])
        self.object.archival_unit = container.archival_unit
        self.object.container = container
        self.object.primary_type = container.primary_type
        if self.object.level == 'I':
            item_no = get_number_of_items(self.object.container.id, self.object.folder_no)
            self.object.sequence_no = item_no + 1
            self.object.archival_reference_code = "%s/%s:%s-%s" % (self.object.container.archival_unit.reference_code,
                                                                   self.object.container.container_no,
                                                                   self.object.folder_no,
                                                                   self.object.sequence_no)
        else:
            self.object.archival_reference_code = "%s/%s:%s" % (self.object.container.archival_unit.reference_code,
                                                                self.object.container.container_no,
                                                                self.object.folder_no)
        return super(FindingAidsCreate, self).forms_valid(form, formset)


class FindingAidsUpdate(FindingAidsPermissionMixin, AuditTrailContextMixin, FindingAidsAllowedArchivalUnitMixin,
                        InlineSuccessMessageMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = FindingAidsEntity
    form_class = FindingAidsUpdateForm
    template_name = 'finding_aids/container_view/form.html'
    success_message = ugettext("%(title)s was updated successfully")
    inlines = [FindingAidsAssociatedPeopleInline, FindingAidsAssociatedCorporationInline,
               FindingAidsAssociatedCountryInline, FindingAidsAssociatedPlaceInline, FindingAidsLanguageInline,
               FindingAidsExtentInline]
    inlines_names = ['associated_people', 'associated_corporations', 'associated_countries', 'associated_places',
                     'languages', 'extents']

    def get_success_url(self):
        return reverse_lazy('finding_aids:finding_aids_container_list',
                            kwargs={'container_id': self.object.container.id})

    def get_context_data(self, **kwargs):
        context = super(FindingAidsUpdate, self).get_context_data(**kwargs)
        context['container'] = self.object.container
        return context

    def get_initial(self):
        initial = {'level_hidden': self.object.level}
        return initial

    def forms_valid(self, form, formset):
        container = Container.objects.get(pk=self.kwargs['container_id'])
        self.object.archival_unit = container.archival_unit
        self.object.container = container
        self.object.primary_type = container.primary_type
        return super(FindingAidsUpdate, self).forms_valid(form, formset)


class FindingAidsCreateFromTemplate(FindingAidsCreate):
    def get_initial(self):
        template = FindingAidsEntity.objects.get(pk=self.kwargs['template_id'])
        container = Container.objects.get(pk=self.kwargs['container_id'])
        return collect_initial(template, container)

    def get_inlines(self):
        template = FindingAidsEntity.objects.get(pk=self.kwargs['template_id'])
        inlines = super(FindingAidsCreateFromTemplate, self).get_inlines()
        return self.collect_inline_initials(template, inlines)

    @staticmethod
    def collect_inline_initials(template, inlines):
        pass
        for idx, inline in enumerate(inlines):
            initials_array = []
            model_name = inline.model._meta.model_name
            fields = [x.name for x in inline.model._meta.fields]
            set_name = "%s_set" % model_name
            for val in getattr(template, set_name).all():
                initial_values = {}
                for field in fields:
                    if getattr(val, field):
                        initial_values[field] = getattr(val, field)
                initial_values.pop('id', None)
                initial_values.pop('fa_entity', None)
                initials_array.append(initial_values)
            inlines[idx].initial = initials_array
        return inlines


def collect_initial(template, container):
    initial = {}

    # SIMPLE FIELDS
    for field in template._meta.fields:
        if not (isinstance(field, AutoField) or isinstance(field, UUIDField) or isinstance(field, ForeignKey)):
            if getattr(template, field.name):
                initial[field.name] = getattr(template, field.name)

    # MANY TO MANY FIELDS
    for field in template._meta.many_to_many:
        initial[field.name] = [int(i.id) for i in getattr(template, field.name).all()]

    # Remove fields
    initial.pop('template_name', None)

    # Set values
    initial['is_template'] = False
    initial['level'] = 'F'
    folder_no = get_number_of_folders(container.id) + 1
    initial['folder_no'] = folder_no
    initial['archival_reference_code'] = "%s/%s:%s" % (container.archival_unit.reference_code,
                                                       container.container_no, folder_no)
    return initial


class FindingAidsClone(FindingAidsPermissionMixin, JSONResponseMixin, DetailView):
    model = FindingAidsEntity

    def post(self, request, *args, **kwargs):
        old_obj = FindingAidsEntity.objects.get(pk=kwargs['pk'])
        new_obj = old_obj.clone()

        renumber_entries("clone", new_obj.level, new_obj.folder_no, new_obj.sequence_no)
        new_numbers = new_number(new_obj=new_obj)

        new_obj.folder_no = new_numbers['folder_no']
        new_obj.sequence_no = new_numbers['sequence_no']

        new_obj.save()
        context = {'success': 'ok'}
        return self.render_json_response(context)


class FindingAidsDelete(FindingAidsPermissionMixin, AjaxDeleteView):
    model = FindingAidsEntity
    template_name = 'finding_aids/container_view/delete.html'
    context_object_name = 'finding_aids'
    success_message = ugettext("Finding Aids record was deleted successfully!")

    def get_success_url(self):
        container = self.object.container
        return reverse_lazy('finding_aids:finding_aids_container_list', kwargs={'container_id': container.id})

    def get_success_message(self):
        return self.success_message

    def get_success_result(self):
        return {'status': 'ok', 'message': self.get_success_message()}

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        self.object.delete()

        level = self.object.level
        folder_no = self.object.folder_no
        sequence_no = self.object.sequence_no
        renumber_entries("delete", level, folder_no, sequence_no)

        if self.request.is_ajax():
            return self.render_json_response(self.get_success_result())
        else:
            return HttpResponseRedirect(success_url)
