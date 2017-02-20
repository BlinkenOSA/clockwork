from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView

from archival_unit.forms import FondsCreateForm, FondsUpdateForm, SubFondsCreateForm, \
    SubFondsUpdateForm, SeriesCreateForm, SeriesUpdateForm
from archival_unit.models import ArchivalUnit


'''
    *************
    Fonds Classes
    *************
'''


class FondsList(ListView):
    template_name = 'archival_unit/fonds.html'
    context_object_name = 'fonds'

    def get_queryset(self):
        return ArchivalUnit.objects.filter(level='F')


class FondsListJson(BaseDatatableView):
    columns = ['sort', 'reference_code', 'title', 'acronym', 'navigate', 'action']
    order_columns = ['sort', 'sort', '', '', '', '']
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
            return render_to_string('archival_unit/fonds_navigate_buttons.html', context={'id': row.id})
        elif column == 'action':
            return render_to_string('archival_unit/fonds_action_buttons.html', context={'id': row.id})
        else:
            return super(FondsListJson, self).render_column(row, column)


class FondsCreate(SuccessMessageMixin, CreateView):
    model = ArchivalUnit
    form_class = FondsCreateForm
    template_name = 'archival_unit/fonds_create_form.html'
    success_url = reverse_lazy('archival_unit:fonds')
    success_message = ugettext("HU-OSA %(fonds)s was created successfully")

    def get_initial(self):
        return {
            'level': 'F',
            'subfonds': 0,
            'series': 0
        }


class FondsUpdate(SuccessMessageMixin, UpdateView):
    model = ArchivalUnit
    form_class = FondsUpdateForm
    template_name = 'archival_unit/fonds_edit_form.html'
    success_url = reverse_lazy('archival_unit:fonds')
    success_message = ugettext("HU-OSA %(fonds)s was updated successfully")


class FondsDelete(DeleteView):
    model = ArchivalUnit
    template_name = 'archival_unit/fonds_delete.html'
    context_object_name = 'fonds'
    success_url = reverse_lazy('archival_unit:fonds')
    success_message = ugettext("Fonds was deleted successfully")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(FondsDelete, self).delete(request, *args, **kwargs)

'''
    ****************
    Subfonds Classes
    ****************
'''


class SubFondsList(ListView):
    template_name = 'archival_unit/subfonds.html'
    context_object_name = 'fonds'

    def get_queryset(self):
        return ArchivalUnit.objects.get(pk=self.kwargs['parent_id'])


class SubFondsListJson(BaseDatatableView):
    columns = ['sort', 'reference_code', 'title', 'acronym', 'navigate', 'action']
    order_columns = ['sort', 'sort']
    max_display_length = 500

    def get_initial_queryset(self):
        return ArchivalUnit.objects.filter(parent=ArchivalUnit.objects.get(pk=self.kwargs['parent_id']))

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
            return render_to_string('archival_unit/subfonds_navigate_buttons.html', context={'id': row.id})
        elif column == 'action':
            return render_to_string('archival_unit/subfonds_action_buttons.html', context={'parent_id': row.parent.id,
                                                                                           'id': row.id})
        else:
            return super(SubFondsListJson, self).render_column(row, column)


class SubFondsCreate(SuccessMessageMixin, CreateView):
    model = ArchivalUnit
    form_class = SubFondsCreateForm
    template_name = 'archival_unit/subfonds_create_form.html'
    success_message = ugettext("HU-OSA %(fonds)s-%(subfonds)s was created successfully")

    def get_success_url(self):
        parent_id = self.kwargs['parent_id']
        return reverse('archival_unit:subfonds', kwargs={'parent_id': parent_id} )

    def get_initial(self):
        fonds = ArchivalUnit.objects.get(pk=self.kwargs['parent_id'])
        initial = super(SubFondsCreate, self).get_initial()
        initial['fonds_title'] = fonds.title
        initial['parent'] = fonds.id
        initial['fonds'] = fonds.fonds
        initial['series'] = 0
        initial['level'] = 'SF'
        return initial


class SubFondsUpdate(SuccessMessageMixin, UpdateView):
    model = ArchivalUnit
    form_class = SubFondsUpdateForm
    template_name = 'archival_unit/subfonds_edit_form.html'
    success_message = ugettext("HU-OSA %(fonds)s-%(subfonds)s was updated successfully")

    def get_success_url(self):
        parent_id = self.kwargs['parent_id']
        return reverse('archival_unit:subfonds', kwargs={'parent_id': parent_id} )

    def get_initial(self):
        fonds = ArchivalUnit.objects.get(pk=self.kwargs['parent_id'])
        initial = super(SubFondsUpdate, self).get_initial()
        initial['fonds_title'] = fonds.title
        return initial


class SubFondsDelete(DeleteView):
    model = ArchivalUnit
    template_name = 'archival_unit/subfonds_delete.html'
    context_object_name = 'subfonds'
    success_message = ugettext("Subfonds was deleted successfully")

    def get_success_url(self):
        parent_id = self.kwargs['parent_id']
        return reverse('archival_unit:subfonds', kwargs={'parent_id': parent_id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(SubFondsDelete, self).delete(request, *args, **kwargs)

'''
    **************
    Series Classes
    **************
'''


class SeriesList(ListView):
    template_name = 'archival_unit/series.html'
    context_object_name = 'subfonds'

    def get_queryset(self):
        return ArchivalUnit.objects.get(pk=self.kwargs['parent_id'])


class SeriesListJson(BaseDatatableView):
    columns = ['sort', 'reference_code', 'title', 'acronym', 'action']
    order_columns = ['sort', 'sort']
    max_display_length = 500

    def get_initial_queryset(self):
        return ArchivalUnit.objects.filter(parent=ArchivalUnit.objects.get(pk=self.kwargs['parent_id']))

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
            return render_to_string('archival_unit/series_action_buttons.html', context={'parent_id': row.parent.id,
                                                                                         'id': row.id})
        else:
            return super(SeriesListJson, self).render_column(row, column)


class SeriesCreate(SuccessMessageMixin, CreateView):
    model = ArchivalUnit
    form_class = SeriesCreateForm
    template_name = 'archival_unit/series_create_form.html'
    success_message = ugettext("HU-OSA %(fonds)s-%(subfonds)s-%(series)s was created successfully")

    def get_success_url(self):
        parent_id = self.kwargs['parent_id']
        return reverse('archival_unit:series', kwargs={'parent_id': parent_id})

    def get_initial(self):
        subfonds = ArchivalUnit.objects.get(pk=self.kwargs['parent_id'])
        fonds = ArchivalUnit.objects.get(pk=subfonds.parent_id)
        initial = super(SeriesCreate, self).get_initial()
        initial['fonds'] = fonds.fonds
        initial['fonds_title'] = fonds.title
        initial['subfonds'] = subfonds.subfonds
        initial['subfonds_title'] = subfonds.title
        initial['parent'] = subfonds.id
        initial['series'] = 0
        initial['level'] = 'S'
        return initial


class SeriesUpdate(SuccessMessageMixin, UpdateView):
    model = ArchivalUnit
    form_class = SeriesUpdateForm
    template_name = 'archival_unit/series_edit_form.html'
    success_message = ugettext("HU-OSA %(fonds)s-%(subfonds)s-%(series)s was updated successfully")

    def get_success_url(self):
        parent_id = self.kwargs['parent_id']
        return reverse('archival_unit:series', kwargs={'parent_id': parent_id})

    def get_initial(self):
        subfonds = ArchivalUnit.objects.get(pk=self.kwargs['parent_id'])
        fonds = ArchivalUnit.objects.get(pk=subfonds.parent.id)
        initial = super(SeriesUpdate, self).get_initial()
        initial['fonds_title'] = fonds.title
        initial['subfonds_title'] = subfonds.title
        return initial


class SeriesDelete(DeleteView):
    model = ArchivalUnit
    template_name = 'archival_unit/series_delete.html'
    context_object_name = 'series'
    success_message = ugettext("Series was deleted successfully")

    def get_success_url(self):
        parent_id = self.kwargs['parent_id']
        return reverse('archival_unit:series', kwargs={'parent_id': parent_id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(SeriesDelete, self).delete(request, *args, **kwargs)