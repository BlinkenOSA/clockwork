from django.db.models import AutoField, UUIDField, ForeignKey
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
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
               FindingAidsExtentInline, FindingAidsDateInline]
    inlines_names = ['associated_people', 'associated_corporations', 'associated_countries', 'associated_places',
                     'languages', 'extents', 'dates']

    def get_success_url(self):
        return reverse_lazy('finding_aids:finding_aids_container_list',
                            kwargs={'container_id': self.kwargs['container_id']})

    def get_initial(self):
        initial = {}
        container = Container.objects.get(pk=self.kwargs['container_id'])
        initial['description_level'] = 'L1'
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
        if self.object.description_level == 'L2':
            item_no = get_number_of_items(self.object.container.id, self.object.folder_no)
            self.object.sequence_no = item_no + 1
            self.object.archival_reference_code = "%s:%s/%s-%s" % (self.object.container.archival_unit.reference_code,
                                                                   self.object.container.container_no,
                                                                   self.object.folder_no,
                                                                   self.object.sequence_no)
        else:
            self.object.archival_reference_code = "%s:%s/%s" % (self.object.container.archival_unit.reference_code,
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
               FindingAidsExtentInline, FindingAidsDateInline]
    inlines_names = ['associated_people', 'associated_corporations', 'associated_countries', 'associated_places',
                     'languages', 'extents', 'dates']

    def get_success_url(self):
        return reverse_lazy('finding_aids:finding_aids_container_list',
                            kwargs={'container_id': self.object.container.id})

    def get_context_data(self, **kwargs):
        context = super(FindingAidsUpdate, self).get_context_data(**kwargs)
        context['container'] = self.object.container
        return context

    def forms_valid(self, form, formset):
        container = Container.objects.get(pk=self.kwargs['container_id'])
        self.object.archival_unit = container.archival_unit
        self.object.container = container
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
    initial['description_level'] = 'L1'
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

        renumber_entries("clone", new_obj)
        new_numbers = new_number(new_obj=new_obj)

        new_obj.folder_no = new_numbers['folder_no']
        new_obj.sequence_no = new_numbers['sequence_no']

        new_obj.title += " [copy]"

        new_obj.published = False
        new_obj.user_published = ""
        new_obj.date_published = None

        new_obj.save()
        context = {'success': 'ok'}
        return self.render_json_response(context)


class FindingAidsDelete(FindingAidsPermissionMixin, AjaxDeleteView):
    model = FindingAidsEntity
    template_name = 'finding_aids/container_view/delete.html'
    context_object_name = 'finding_aids'
    success_message = ugettext("Finding Aids record was deleted successfully!")

    def get_success_url(self):
        container = self.obj.container
        return reverse_lazy('finding_aids:finding_aids_container_list', kwargs={'container_id': container.id})

    def get_success_message(self):
        return self.success_message

    def get_success_result(self):
        return {'status': 'ok', 'message': self.get_success_message()}

    def delete(self, request, *args, **kwargs):
        self.obj = self.get_object()
        success_url = self.get_success_url()

        self.obj.delete()
        renumber_entries("delete", self.obj)

        if self.request.is_ajax():
            return self.render_json_response(self.get_success_result())
        else:
            return HttpResponseRedirect(success_url)


class FindingAidsAction(FindingAidsPermissionMixin, FindingAidsAllowedArchivalUnitMixin, JSONResponseMixin, DetailView):
    model = FindingAidsEntity

    def post(self, request, *args, **kwargs):
        actions = ['publish', 'unpublish', 'set_confidential', 'unset_confidential']
        action = self.kwargs['action']
        container = self.kwargs['container_id']
        pk = self.kwargs['pk']

        if action in actions:
            if pk == 'all':
                finding_aids_entities = FindingAidsEntity.objects.filter(container=container)
            else:
                finding_aids_entities = [self.get_object(), ]

            for finding_aids in finding_aids_entities:
                if action == 'publish':
                    finding_aids.publish(request.user)
                if action == 'unpublish':
                    finding_aids.unpublish()
                if action == 'set_confidential':
                    finding_aids.set_confidential()
                if action == 'unset_confidential':
                    finding_aids.unset_confidential()

            if pk == 'all':
                context = {
                    'status': 'ok'
                }
            else:
                finding_aids = finding_aids_entities[0]
                dates = [str(finding_aids.date_from) if finding_aids.date_from else "",
                         str(finding_aids.date_to) if finding_aids.date_to else ""]

                folder_no = finding_aids.container.archival_unit.reference_code + '/' + \
                    str(finding_aids.container.container_no) + ':' + str(finding_aids.folder_no)

                if finding_aids.level == 'F':
                    icon = '<i class="fa fa-folder-open-o"></i>'
                else:
                    icon = '<i class="fa fa-file-o"></i>'

                if finding_aids.description_level == 'L1':
                    level = '<span class="call_no_level_1">' + icon + folder_no + '</span>'
                else:
                    level = '<span class="call_no_level_2">' + icon + folder_no + '-' \
                            + str(finding_aids.sequence_no) + '</span>'

                context = {
                    'DT_rowId': finding_aids.id,
                    'level': level,
                    'title': finding_aids.title,
                    'title_original': finding_aids.title_original,
                    'date':  ' - '.join(filter(None, dates)),
                    'action': render_to_string('finding_aids/container_view/table_action_buttons.html',
                                               context={'container_id': finding_aids.container.id,
                                                        'id': finding_aids.id,
                                                        'published': finding_aids.published,
                                                        'catalog_id': finding_aids.catalog_id}),
                    'publish': render_to_string('finding_aids/container_view/table_publish_buttons.html', context={
                        'finding_aids_entity': finding_aids
                    })
                }

            return self.render_json_response(context)
        else:
            return self.render_json_response(None)