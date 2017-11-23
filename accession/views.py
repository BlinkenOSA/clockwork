from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import DetailView, TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from extra_views import NamedFormsetsMixin, CreateWithInlinesView, UpdateWithInlinesView
from datetime import date

from accession.form import AccessionForm, AccessionItemsInlineForm
from accession.models import Accession
from clockwork.ajax_extra_views import AjaxDeleteProtectedView
from clockwork.mixins import InlineSuccessMessageMixin, GeneralAllPermissionMixin, AuditTrailContextMixin


class AccessionPermissionMixin(GeneralAllPermissionMixin):
    permission_model = Accession


class AccessionList(AccessionPermissionMixin, TemplateView):
    template_name = 'accession/list.html'


class AccessionListJson(AccessionPermissionMixin, BaseDatatableView):
    model = Accession
    columns = ['seq', 'transfer_date', 'title', 'action']
    order_columns = ['seq', 'transfer_date', 'title', '']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(title__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            number_of_archival_units = row.archivalunit_set.all().count()
            return render_to_string('accession/table_action_buttons.html',
                                    context={'id': row.id, 'number_of_archival_units': number_of_archival_units})
        elif column == 'transfer_date':
            return str(row.transfer_date)
        else:
            return super(AccessionListJson, self).render_column(row, column)


class AccessionDetail(AccessionPermissionMixin, DetailView):
    model = Accession
    template_name = 'accession/detail.html'
    context_object_name = 'accession'


class AccessionCreate(AccessionPermissionMixin, InlineSuccessMessageMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Accession
    form_class = AccessionForm
    template_name = 'accession/form.html'
    success_url = reverse_lazy('accession:list')
    success_message = ugettext("Accession Record %(seq)s was created successfully")
    inlines = [AccessionItemsInlineForm]
    inlines_names = ['accession_items']

    def get_initial(self):
        year = date.today().year
        sequence = Accession.objects.filter(date_created__year=year).count()
        return {
            'seq': '%d/%03d' % (year, sequence + 1)
        }


class AccessionUpdate(AccessionPermissionMixin, AuditTrailContextMixin, InlineSuccessMessageMixin,
                      NamedFormsetsMixin, UpdateWithInlinesView):
    model = Accession
    form_class = AccessionForm
    template_name = 'accession/form.html'
    success_url = reverse_lazy('accession:list')
    success_message = ugettext("Accession Record %(seq)s was updated successfully")
    inlines = [AccessionItemsInlineForm]
    inlines_names = ['accession_items']


class AccessionDelete(AccessionPermissionMixin, AjaxDeleteProtectedView):
    model = Accession
    template_name = 'accession/delete.html'
    context_object_name = 'accession'
    success_message = ugettext("Container was deleted successfully!")
    error_message = ugettext("Container is not empty, please select an empty one to delete!")
