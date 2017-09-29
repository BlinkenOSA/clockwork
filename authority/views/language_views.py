from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from fm.views import AjaxCreateView, AjaxUpdateView

from authority.forms import LanguageForm
from authority.models import Language, PersonOtherFormat, CorporationOtherFormat
from clockwork.ajax_extra_views import AjaxDeleteProtectedView
from clockwork.mixins import GeneralAllPermissionMixin
from finding_aids.models import FindingAidsEntityLanguage


class LanguagePermissionMixin(GeneralAllPermissionMixin):
    permission_model = Language


class LanguageList(LanguagePermissionMixin, TemplateView):
    template_name = 'authority/language/list.html'


class LanguageListJson(LanguagePermissionMixin, BaseDatatableView):
    model = Language
    columns = ['id', 'language', 'authority_url', 'iso_639_1', 'iso_639_2', 'action']
    order_columns = ['language', 'iso_639_1', 'iso_639_2']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(language__icontains=search) |
                Q(iso_639_1__icontains=search) |
                Q(iso_639_1__icontains=search)
            )
        return qs

    def render_column(self, row, column):
        if column == 'action':
            fa_language_exists = FindingAidsEntityLanguage.objects.filter(language=row).exists()
            person_other_exists = PersonOtherFormat.objects.filter(language=row).exists()
            corporation_other_exists = CorporationOtherFormat.objects.filter(language=row).exists()
            exists = fa_language_exists or person_other_exists or corporation_other_exists

            return render_to_string('authority/language/table_action_buttons.html',
                                    context={'id': row.id, 'exists': exists})
        elif column == 'authority_url':
            return '<a href="%s" target="_blank">%s</a>' % (row.authority_url, row.authority_url) \
                if row.authority_url else None
        else:
            return super(LanguageListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class LanguageCreate(LanguagePermissionMixin, AjaxCreateView):
    form_class = LanguageForm
    model = Language
    template_name = 'authority/language/form.html'

    def get_response_message(self):
        return ugettext("Language: %s was created successfully!") % self.object.language


class LanguageUpdate(LanguagePermissionMixin, AjaxUpdateView):
    form_class = LanguageForm
    model = Language
    template_name = 'authority/language/form.html'

    def get_response_message(self):
        return ugettext("Language: %s was updated successfully!") % self.object.language


class LanguageDelete(LanguagePermissionMixin, AjaxDeleteProtectedView):
    model = Language
    template_name = 'authority/language/delete.html'
    context_object_name = 'language'
    success_message = ugettext("Language was deleted successfully!")
    error_message = ugettext("Language can't be deleted, because it has already been assigned to an entry!")