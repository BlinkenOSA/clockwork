from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q, ProtectedError
from fm.views import AjaxCreateView, AjaxDeleteView

from accession.models import Accession
from clockwork.mixins import GeneralAllPermissionMixin, AuditTrailContextMixin
from donor.models import Donor
from donor.forms import DonorForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, TemplateView


class DonorPermissionMixin(GeneralAllPermissionMixin):
    permission_model = Donor


class DonorList(DonorPermissionMixin, TemplateView):
    template_name = 'donor/list.html'


class DonorListJson(DonorPermissionMixin, BaseDatatableView):
    model = Donor
    columns = ['id', 'name', 'address', 'action']
    order_columns = ['id', 'name', '', '']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(country__country__icontains=search) |
                Q(city__icontains=search) |
                Q(address__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'address':
            return row.get_address()
        elif column == 'action':
            accesson_exist = Accession.objects.filter(donor=row).exists()
            return render_to_string('donor/table_action_buttons.html',
                                    context={'id': row.id, 'accession_exist': accesson_exist})
        else:
            return super(DonorListJson, self).render_column(row, column)


class DonorDetail(DonorPermissionMixin, DetailView):
    model = Donor
    template_name = 'donor/detail.html'
    context_object_name = 'donor'


class DonorCreate(DonorPermissionMixin, SuccessMessageMixin, CreateView):
    model = Donor
    form_class = DonorForm
    template_name = 'donor/form.html'
    success_url = reverse_lazy('donor:list')
    success_message = ugettext("%(name)s was created successfully")


class DonorUpdate(DonorPermissionMixin, AuditTrailContextMixin, SuccessMessageMixin, UpdateView):
    model = Donor
    form_class = DonorForm
    template_name = 'donor/form.html'
    success_url = reverse_lazy('donor:list')
    success_message = ugettext("%(name)s was updated successfully")


class DonorDelete(DonorPermissionMixin, AjaxDeleteView):
    model = Donor
    template_name = 'donor/delete.html'
    context_object_name = 'donor'

    def get_success_result(self):
        msg = ugettext("Donor: %s was deleted successfully!") % self.object.name
        return {'status': 'ok', 'message': msg}

    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.pre_delete()
            self.object.delete()
            self.post_delete()
            if self.request.is_ajax():
                return self.render_json_response(self.get_success_result())
        except ProtectedError:
                return self.render_json_response({'status': 'error',
                                                  'message': ugettext('Donor is referenced, please select a donor'
                                                                      'record which is not selected elsewhere!')})

        return HttpResponseRedirect(self.get_success_url())


class DonorPopupCreate(DonorPermissionMixin, SuccessMessageMixin, AjaxCreateView):
    model = Donor
    form_class = DonorForm
    template_name = 'donor/popup/form_popup.html'

    def get_success_result(self):
        return {
            'status': 'ok',
            'message': self.get_response_message(),
            'entry_id': self.object.id,
            'entry_name': self.object.name
        }