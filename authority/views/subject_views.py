from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext
from django.views.generic import TemplateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from authority.forms import SubjectForm
from authority.models import Subject


class SubjectList(TemplateView):
    template_name = 'authority/subject/list.html'


class SubjectListJson(BaseDatatableView):
    model = Subject
    columns = ['id', 'subject', 'authority_url', 'action']
    order_columns = ['subject']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(subject__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            return render_to_string('authority/subject/table_action_buttons.html', context={'id': row.id})
        elif column == 'authority_url':
            return '<a href="%s" target="_blank">%s</a>' % (row.authority_url, row.authority_url) \
                if row.authority_url else None
        else:
            return super(SubjectListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class SubjectCreate(AjaxCreateView):
    form_class = SubjectForm
    model = Subject
    template_name = 'authority/subject/form.html'

    def get_response_message(self):
        return ugettext("Subject: %s was created successfully!") % self.object


class SubjectUpdate(AjaxUpdateView):
    form_class = SubjectForm
    model = Subject
    template_name = 'authority/subject/form.html'

    def get_response_message(self):
        return ugettext("Subject: %s was updated successfully!") % self.object


class SubjectDelete(DeleteView):
    model = Subject
    template_name = 'authority/subject/delete.html'
    context_object_name = 'subject'
    success_url = reverse_lazy('authority:subject_list')
    success_message = ugettext("Subject was deleted successfully")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(SubjectDelete, self).delete(request, *args, **kwargs)

