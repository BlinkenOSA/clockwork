from django.forms import ModelChoiceField, Form, ModelForm, Textarea
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from extra_views import InlineFormSet

from archival_unit.models import ArchivalUnit
from archival_unit.widgets import ArchivalUnitSeriesSelect2Widget
from authority.models import Person

from controlled_list.models import Locale
from finding_aids.models import FindingAidsEntity, FindingAidsEntityAssociatedPerson

IMG_FLAG = ' <span class="flag"></span>'


class FindingAidsArchivalUnitForm(Form):
    archival_unit = ModelChoiceField(
        queryset=ArchivalUnit.objects.filter(level='S').order_by('fonds', 'subfonds', 'series'),
        widget=ArchivalUnitSeriesSelect2Widget()
    )


class FindingAidsForm(ModelForm):
    original_locale = ModelChoiceField(empty_label=ugettext('- Select Original Locale -'),
                                       queryset=Locale.objects.all(), required=False)

    class Meta:
        model = FindingAidsEntity
        fields = '__all__'
        labels = {
            'title_original': mark_safe(ugettext('Title - Original Language') + IMG_FLAG),
            'contents_summary_original': mark_safe(ugettext('Contents Summary - Original Language') + IMG_FLAG)
        }
        widgets = {
            'contents_summary': Textarea(attrs={'rows': 3}),
            'contents_summary_original': Textarea(attrs={'rows': 3}),
        }
        help_texts = {
            'date_from': 'Date format: YYYY, or YYYY-MM, or YYYY-MM-DD',
            'date_to': 'Date format: YYYY, or YYYY-MM, or YYYY-MM-DD'
        }


class FindingAidsAssociatedPeopleInline(InlineFormSet):
    extra = 1
    model = FindingAidsEntityAssociatedPerson
    fields = '__all__'
    can_delete = True
    prefix = 'associated_people'




