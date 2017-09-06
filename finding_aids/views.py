from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext
from django.views.generic import FormView, ListView, TemplateView, DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView
from extra_views import NamedFormsetsMixin, CreateWithInlinesView, UpdateWithInlinesView
from fm.views import JSONResponseMixin, AjaxDeleteView

from clockwork.mixins import InlineSuccessMessageMixin
from container.models import Container
from finding_aids.forms import FindingAidsArchivalUnitForm, FindingAidsForm, FindingAidsAssociatedPeopleInline, \
    FindingAidsAssociatedCorporationInline, FindingAidsAssociatedCountryInline, FindingAidsAssociatedPlaceInline, \
    FindingAidsLanguageInline, FindingAidsExtentInline, FindingAidsUpdateForm
from finding_aids.models import FindingAidsEntity


class FindingAidsArchivalUnit(FormView):
    template_name = 'finding_aids/select_archival_unit/select_archival_unit.html'
    form_class = FindingAidsArchivalUnitForm


class FindingAidsInContainerList(TemplateView):
    template_name = 'finding_aids/container_view/list.html'

    def get_context_data(self, **kwargs):
        context = super(FindingAidsInContainerList, self).get_context_data(**kwargs)
        context['container'] = Container.objects.get(pk=kwargs['container_id'])
        return context


class FindingAidsInContainerListJson(BaseDatatableView):
    model = FindingAidsEntity
    columns = ['level', 'title', 'title_original', 'date', 'action']
    order_columns = ['folder_no', 'sequence_no', 'title']
    max_display_length = 500

    def get_initial_queryset(self):
        container = Container.objects.get(pk=self.kwargs['container_id'])
        finding_aids_entities = FindingAidsEntity.objects.filter(container=container).order_by('folder_no')
        return finding_aids_entities

    def render_column(self, row, column):
        if column == 'level':
            folder_no = row.container.archival_unit.reference_code + '/' + str(row.container.container_no) + \
                        ':' + str(row.folder_no)
            if row.level == 'F':
                icon = '<i class="fa fa-folder-open-o"></i>'
                return '<span class="call_no_folder">' + icon + folder_no + '</span>'
            else:
                icon = '<i class="fa fa-file-o"></i>'
                return '<span class="call_no_item">' + icon + folder_no + '-' + str(row.sequence_no) + '</span>'
        elif column == 'date':
            dates = [str(row.date_from) if row.date_from else "", str(row.date_to) if row.date_to else ""]
            return ' - '.join(filter(None, dates))
        elif column == 'action':
            return render_to_string('finding_aids/container_view/table_action_buttons.html', context={
                'container_id': row.container_id, 'id': row.id})
        else:
            return super(FindingAidsInContainerListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class FindingAidsCreate(InlineSuccessMessageMixin, NamedFormsetsMixin, CreateWithInlinesView):
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


class FindingAidsUpdate(InlineSuccessMessageMixin, NamedFormsetsMixin, UpdateWithInlinesView):
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
        self.object.container = container
        self.object.primary_type = container.primary_type
        return super(FindingAidsUpdate, self).forms_valid(form, formset)


class FindingAidsClone(JSONResponseMixin, DetailView):
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

    def renumber_entries(self, new_obj):
        pass


class FindingAidsDelete(AjaxDeleteView):
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


class FindingAidsNewFolderNumber(JSONResponseMixin, ListView):
    model = FindingAidsEntity

    def get(self, request, *args, **kwargs):
        stats = {}

        folder_no = get_number_of_folders(kwargs['container_id'])

        container = Container.objects.get(pk=kwargs['container_id'])
        arc = "%s/%s:%s" % (container.archival_unit.reference_code,
                            container.container_no,
                            folder_no + 1)

        stats['new_folder'] = folder_no + 1
        stats['new_arc'] = arc
        return self.render_json_response({'stats': stats})


class FindingAidsNewItemNumber(JSONResponseMixin, ListView):
    model = FindingAidsEntity

    def get(self, request, *args, **kwargs):
        stats = {}
        item_no = get_number_of_items(kwargs['container_id'], kwargs['folder_no'])

        container = Container.objects.get(pk=kwargs['container_id'])
        arc = "%s/%s:%s-%s" % (container.archival_unit.reference_code,
                               container.container_no,
                               kwargs['folder_no'],
                               item_no + 1)

        stats['new_item'] = item_no + 1
        stats['new_arc'] = arc
        return self.render_json_response({'stats': stats})


def get_number_of_folders(container_id):
    return FindingAidsEntity.objects.filter(container=Container.objects.get(pk=container_id))\
                                    .values('folder_no').distinct().count()


def get_number_of_items(container_id, folder_no):
    return FindingAidsEntity.objects.filter(level='I')\
        .filter(container=Container.objects.get(pk=container_id))\
        .filter(folder_no=folder_no)\
        .count()


def new_number(new_obj):
    if new_obj.level == 'F':
        return {'folder_no': new_obj.folder_no + 1, 'sequence_no': 0}
    else:
        return {'folder_no': new_obj.folder_no, 'sequence_no': new_obj.sequence_no + 1}


def renumber_entries(action, level, folder_no, sequence_no):
    if action == 'delete':
        step = -1
    else:
        step = 1

    if level == 'F':
        folders = FindingAidsEntity.objects.filter(folder_no__gt=folder_no)
        for folder in folders:
            folder.folder_no += step
            folder.save()
    else:
        items = FindingAidsEntity.objects.filter(folder_no=folder_no,
                                                 sequence_no__gt=sequence_no)
        if len(items) > 0:
            for item in items:
                item.sequence_no += step
                item.save()
        else:
            folders = FindingAidsEntity.objects.filter(folder_no__gt=folder_no)
            for folder in folders:
                folder.folder_no += step
                folder.save()
