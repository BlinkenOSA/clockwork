from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import FormMixin
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView

from archival_unit.forms import FondsCreateForm, FondsUpdateForm, SubFondsCreateForm, \
    SubFondsUpdateForm, SeriesCreateForm, SeriesUpdateForm
from archival_unit.models import ArchivalUnit


'''
    *************
    Fonds Classes
    *************
'''


class FondsList(FormMixin, ListView):
    template_name = 'archival_unit/fonds.html'
    context_object_name = 'fonds'
    form_class = FondsCreateForm

    def get_queryset(self):
        return ArchivalUnit.objects.filter(level='F')


class FondsListJson(BaseDatatableView):
    columns = ['sort', 'reference_code', 'title', 'navigate', 'action']
    order_columns = ['sort', 'sort', '', '', '']
    max_display_length = 500

    def get_initial_queryset(self):
        return ArchivalUnit.objects.filter(level='F')

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(reference_code__icontains=search) |
                Q(title__icontains=search) |
                Q(acronym__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'navigate':
            return render_to_string('archival_unit/fonds_navigate_buttons.html', context={'id': row.reference_code_id})
        elif column == 'action':
            return render_to_string('archival_unit/fonds_action_buttons.html', context={'id': row.reference_code_id})
        else:
            return super(FondsListJson, self).render_column(row, column)


class FondsCreate(AjaxCreateView):
    model = ArchivalUnit
    form_class = FondsCreateForm
    template_name = 'archival_unit/fonds_form.html'

    def get_initial(self):
        return {
            'level': 'F',
            'subfonds': 0,
            'series': 0
        }

    def get_response_message(self):
        return ugettext("HU OSA %s was created successfully!") % self.object.fonds


class FondsUpdate(AjaxUpdateView):
    form_class = FondsUpdateForm
    template_name = 'archival_unit/fonds_form.html'

    def get_object(self, queryset=None):
        return ArchivalUnit.objects.get(reference_code_id=self.kwargs['reference_code_id'])

    def get_response_message(self):
        return ugettext("%s was updated successfully!") % self.object.reference_code


class FondsDelete(AjaxDeleteView):
    template_name = 'archival_unit/fonds_delete.html'
    context_object_name = 'fonds'

    def get_object(self, queryset=None):
        return ArchivalUnit.objects.get(reference_code_id=self.kwargs['reference_code_id'])

    def get_success_result(self):
        msg = ugettext("Fonds: %s was deleted successfully!") % self.object.reference_code
        return {'status': 'ok', 'message': msg}


'''
    ****************
    Subfonds Classes
    ****************
'''


class SubFondsList(FormMixin, ListView):
    template_name = 'archival_unit/subfonds.html'
    form_class = SubFondsCreateForm
    context_object_name = 'fonds'

    def get_queryset(self):
        return ArchivalUnit.objects.get(reference_code_id=self.kwargs['parent_reference_code_id'])


class SubFondsListJson(BaseDatatableView):
    columns = ['sort', 'reference_code', 'title', 'navigate', 'action']
    order_columns = ['sort', 'sort']
    max_display_length = 500

    def get_initial_queryset(self):
        return ArchivalUnit.objects.filter(parent=ArchivalUnit.objects.get(reference_code_id=self.kwargs['parent_reference_code_id']))

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(reference_code__icontains=search) |
                Q(title__icontains=search) |
                Q(acronym__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'navigate':
            return render_to_string('archival_unit/subfonds_navigate_buttons.html', context={'id': row.reference_code_id})
        elif column == 'action':
            return render_to_string('archival_unit/subfonds_action_buttons.html', context={'id': row.reference_code_id})
        else:
            return super(SubFondsListJson, self).render_column(row, column)


class SubFondsCreate(AjaxCreateView):
    form_class = SubFondsCreateForm
    template_name = 'archival_unit/subfonds_form.html'

    def get_initial(self):
        fonds = ArchivalUnit.objects.get(reference_code_id=self.kwargs['parent_reference_code_id'])
        initial = super(SubFondsCreate, self).get_initial()
        initial['fonds_title'] = fonds.title
        initial['fonds_acronym'] = fonds.acronym
        initial['parent'] = fonds.id
        initial['fonds'] = fonds.fonds
        initial['series'] = 0
        initial['level'] = 'SF'
        return initial

    def get_response_message(self):
        return ugettext("%s was created successfully!") % self.object.reference_code


class SubFondsUpdate(AjaxUpdateView):
    model = ArchivalUnit
    form_class = SubFondsUpdateForm
    template_name = 'archival_unit/subfonds_form.html'

    def get_object(self, queryset=None):
        return ArchivalUnit.objects.get(reference_code_id=self.kwargs['reference_code_id'])

    def get_initial(self):
        fonds = ArchivalUnit.objects.get(reference_code_id=self.kwargs['reference_code_id']).parent
        initial = super(SubFondsUpdate, self).get_initial()
        initial['fonds_title'] = fonds.title
        initial['fonds_acronym'] = fonds.acronym
        return initial

    def get_response_message(self):
        return ugettext("%s was updated successfully!") % self.object.reference_code


class SubFondsDelete(AjaxDeleteView):
    template_name = 'archival_unit/subfonds_delete.html'
    context_object_name = 'subfonds'

    def get_object(self, queryset=None):
        return ArchivalUnit.objects.get(reference_code_id=self.kwargs['reference_code_id'])

    def get_success_result(self):
        msg = ugettext("Subfonds: %s was deleted successfully!") % self.object.reference_code
        return {'status': 'ok', 'message': msg}

'''
    **************
    Series Classes
    **************
'''


class SeriesList(FormMixin, ListView):
    template_name = 'archival_unit/series.html'
    form_class = SeriesCreateForm
    context_object_name = 'subfonds'

    def get_queryset(self):
        return ArchivalUnit.objects.get(reference_code_id=self.kwargs['parent_reference_code_id'])


class SeriesListJson(BaseDatatableView):
    columns = ['sort', 'reference_code', 'title', 'action']
    order_columns = ['sort', 'sort']
    max_display_length = 500

    def get_initial_queryset(self):
        return ArchivalUnit.objects.filter(parent=ArchivalUnit.objects.get(reference_code_id=self.kwargs['parent_reference_code_id']))

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(reference_code__icontains=search) |
                Q(title__icontains=search) |
                Q(acronym__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('archival_unit/series_action_buttons.html', context={'id': row.reference_code_id})
        else:
            return super(SeriesListJson, self).render_column(row, column)


class SeriesCreate(AjaxCreateView):
    model = ArchivalUnit
    form_class = SeriesCreateForm
    template_name = 'archival_unit/series_form.html'

    def get_initial(self):
        subfonds = ArchivalUnit.objects.get(reference_code_id=self.kwargs['parent_reference_code_id'])
        fonds = ArchivalUnit.objects.get(pk=subfonds.parent_id)
        initial = super(SeriesCreate, self).get_initial()
        initial['fonds'] = fonds.fonds
        initial['fonds_title'] = fonds.title
        initial['fonds_acronym'] = fonds.acronym
        initial['subfonds'] = subfonds.subfonds
        initial['subfonds_title'] = subfonds.title
        initial['subfonds_acronym'] = subfonds.acronym
        initial['parent'] = subfonds.id
        initial['series'] = 0
        initial['level'] = 'S'
        return initial

    def get_response_message(self):
        return ugettext("%s was created successfully!") % self.object.reference_code


class SeriesUpdate(AjaxUpdateView):
    form_class = SeriesUpdateForm
    template_name = 'archival_unit/series_form.html'

    def get_object(self, queryset=None):
        return ArchivalUnit.objects.get(reference_code_id=self.kwargs['reference_code_id'])

    def get_initial(self):
        subfonds = ArchivalUnit.objects.get(reference_code_id=self.kwargs['reference_code_id']).parent
        fonds = ArchivalUnit.objects.get(pk=subfonds.parent.id)
        initial = super(SeriesUpdate, self).get_initial()
        initial['fonds_title'] = fonds.title
        initial['fonds_acronym'] = fonds.acronym
        initial['subfonds_title'] = subfonds.title
        initial['subfonds_acronym'] = subfonds.acronym
        return initial

    def get_response_message(self):
        return ugettext("%s was updated successfully!") % self.object.reference_code


class SeriesDelete(AjaxDeleteView):
    model = ArchivalUnit
    template_name = 'archival_unit/series_delete.html'
    context_object_name = 'series'

    def get_object(self, queryset=None):
        return ArchivalUnit.objects.get(reference_code_id=self.kwargs['reference_code_id'])

    def get_success_result(self):
        msg = ugettext("Series: %s was deleted successfully!") % self.object.reference_code
        return {'status': 'ok', 'message': msg}