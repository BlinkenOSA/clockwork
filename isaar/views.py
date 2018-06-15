from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import DetailView, TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from extra_views import CreateWithInlinesView, NamedFormsetsMixin, UpdateWithInlinesView

from clockwork.ajax_extra_views import AjaxDeleteProtectedView
from clockwork.mixins import InlineSuccessMessageMixin, GeneralAllPermissionMixin, AuditTrailContextMixin
from isaar.forms import IsaarForm, OtherNamesInline, StandardizedNamesInline, CorporateBodyIdentifiersInLine, \
    PlacesInline, TYPE_CHOICES, ParallelNamesInline
from isaar.models import Isaar


class IsaarPermissionMixin(GeneralAllPermissionMixin):
    permission_model = Isaar


class IsaarList(IsaarPermissionMixin, TemplateView):
    template_name = 'isaar/list.html'


class IsaarListJson(IsaarPermissionMixin, BaseDatatableView):
    model = Isaar
    columns = ['id', 'name', 'type', 'isad', 'status', 'action']
    order_columns = ['name']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(type__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            isad_exist = row.isad_set.exists()
            return render_to_string('isaar/table_action_buttons.html',
                                    context={'id': row.id, 'exist': isad_exist})
        elif column == 'isad':
            values = list(row.isad_set.values_list('reference_code', flat=True))
            return ', '.join(values)
        elif column == 'type':
            return dict(TYPE_CHOICES)[row.type]
        elif column == 'status':
            if row.status == 'Draft':
                return '<span class="label label-warning">draft</span>'
            else:
                return '<span class="label label-success">final</span>'
        else:
            return super(IsaarListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class IsaarDetail(IsaarPermissionMixin, DetailView):
    model = Isaar
    template_name = 'isaar/detail.html'
    context_object_name = 'isaar'

    def get_context_data(self, **kwargs):
        context = super(IsaarDetail, self).get_context_data(**kwargs)
        context['type'] = dict(TYPE_CHOICES)[self.object.type]
        return context


class IsaarCreate(IsaarPermissionMixin, InlineSuccessMessageMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Isaar
    form_class = IsaarForm
    template_name = 'isaar/form.html'
    success_url = reverse_lazy('isaar:list')
    success_message = ugettext("%(name)s was created successfully")
    inlines = [OtherNamesInline, ParallelNamesInline, StandardizedNamesInline, CorporateBodyIdentifiersInLine, PlacesInline]
    inlines_names = ['other_names', 'parallel_names', 'standardized_names', 'corporate_body_identifiers', 'places']


class IsaarUpdate(IsaarPermissionMixin, AuditTrailContextMixin, InlineSuccessMessageMixin,
                  NamedFormsetsMixin, UpdateWithInlinesView):
    model = Isaar
    form_class = IsaarForm
    template_name = 'isaar/form.html'
    success_url = reverse_lazy('isaar:list')
    success_message = ugettext("%(name)s was updated successfully")
    inlines = [OtherNamesInline, ParallelNamesInline, StandardizedNamesInline, CorporateBodyIdentifiersInLine, PlacesInline]
    inlines_names = ['other_names', 'parallel_names', 'standardized_names', 'corporate_body_identifiers', 'places']


class IsaarDelete(IsaarPermissionMixin, AjaxDeleteProtectedView):
    model = Isaar
    template_name = 'isaar/delete.html'
    context_object_name = 'isaar'
    success_message = ugettext("ISAAR-CPF record was deleted successfully!")
    error_message = ugettext("ISAAR-CPF record can't be deleted, "
                             "because it has already been assigned to another record!")
