from django.forms import ModelForm, Textarea, ModelChoiceField, TextInput
from django.utils.translation import ugettext
from extra_views import InlineFormSet

from accession.models import Accession, AccessionItem, AccessionCopyrightStatus, AccessionMethod
from archival_unit.widgets import ArchivalUnitFondsSelect2Widget
from controlled_list.models import Building
from donor.widgets import DonorSelect2Widget
from isaar.widgets import IsaarRecordsSelect2Widget

TYPE_CHOICES = (
    ('' , ugettext('- Select Entity Type - ')),
    ('P', 'Personal'),
    ('C', 'Corporate Body'),
    ('F', 'Family'),
)


class AccessionForm(ModelForm):
    building = ModelChoiceField(queryset=Building.objects.all(),
                                empty_label=ugettext('- Select Building -'),
                                required=True)
    copyright_status = ModelChoiceField(queryset=AccessionCopyrightStatus.objects.all(),
                                        empty_label=ugettext('- Select Copyright -'),
                                        required=True)
    method = ModelChoiceField(queryset=AccessionMethod.objects.all(),
                              empty_label=ugettext('- Select Accession Method -'),
                              required=True)

    class Meta:
        model = Accession
        exclude = ['user_created', 'date_created', 'user_updated', 'date_updated']
        labels = {
            'seq': ugettext('Accession Number'),
            'archival_unit': ugettext('Archival Unit'),
            'archival_unit_legacy_number': ugettext('Archival Unit Number (Legacy)'),
            'archival_unit_legacy_name': ugettext('Archival Unit Name (Legacy)')
        }
        help_texts = {
            'transfer_date': ugettext('Date format: YYYY, or YYYY-MM, or YYYY-MM-DD'),
            'creation_year_from': ugettext('Date format: YYYY'),
            'creation_year_to': ugettext('Date format: YYYY')
        }
        widgets = {
            'archival_unit': ArchivalUnitFondsSelect2Widget(attrs={'data-placeholder': '- Select Archival Unit -'}),
            'creator': IsaarRecordsSelect2Widget(attrs={'data-placeholder': '- Select Creators -'}),
            'donor': DonorSelect2Widget(attrs={'data-placeholder': '- Select Donor -'}),
            'access_note': Textarea(attrs={'rows': 5}),
            'custodial_history': Textarea(attrs={'rows': 3}),
            'copyright_note': Textarea(attrs={'rows': 3}),
            'note': Textarea(attrs={'rows': 3}),
            'archival_unit_legacy_number': TextInput(attrs={'readonly': 'readonly'}),
            'archival_unit_legacy_name': TextInput(attrs={'readonly': 'readonly'}),
        }


class AccessionItemsForm(ModelForm):
    class Meta:
        fields = ('quantity', 'container', 'content')
        widgets = {
            'quantity': TextInput(attrs={'placeholder': ugettext('Quantity')}),
            'container': TextInput(attrs={'placeholder': ugettext('Container')}),
            'content': TextInput(attrs={'placeholder': ugettext('Content')})
        }


class AccessionItemsInlineForm(InlineFormSet):
    extra = 1
    model = AccessionItem
    can_delete = True
    form_class = AccessionItemsForm
    prefix = 'accession_items'

