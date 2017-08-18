from django.forms import ModelForm, Select, ChoiceField, ModelChoiceField, TextInput
from django.utils.translation import ugettext
from extra_views import InlineFormSet

from authority.widgets import LanguageSelect2MultipleWidget
from isaar.models import Isaar, IsaarOtherName, IsaarRelationship, IsaarStandardizedName, IsaarCorporateBodyIdentifier, \
    IsaarPlaceQualifier, IsaarPlace

TYPE_CHOICES = (
    ('' , ugettext('- Select Entity Type - ')),
    ('P', 'Personal'),
    ('C', 'Corporate Body'),
    ('F', 'Family'),
)


class IsaarForm(ModelForm):
    class Meta:
        model = Isaar
        fields = ('name', 'type', 'date_existence_from', 'date_existence_to', 'function', 'legal_status',
                  'general_context', 'history', 'mandate', 'internal_structure',
                  'old_id', 'language', 'level_of_detail', 'status', 'institution_identifier', 'source',
                  'internal_note', 'convention')
        labels = {
            'name': ugettext('Authorized forms of name'),
            'type': ugettext('Type of entity'),
            'old_id': ugettext('Authority record identifier'),
            'language': ugettext('Languages'),
            'convention': ugettext('Rules and/or conventions')
        }
        help_texts = {
            'date_existence_from': ugettext('Date format: YYYY, or YYYY-MM, or YYYY-MM-DD'),
            'date_existence_to': ugettext('Date format: YYYY, or YYYY-MM, or YYYY-MM-DD')
        }
        widgets = {
            'type': Select(choices=TYPE_CHOICES),
            'language': LanguageSelect2MultipleWidget
        }


class OtherNamesForm(ModelForm):
    relationship = ModelChoiceField(queryset=IsaarRelationship.objects.all(),
                                    empty_label=ugettext('- Select Relationship -'),
                                    required=False)

    class Meta:
        model = IsaarOtherName
        fields = ('name', 'year_from', 'year_to')
        widgets = {
            'name': TextInput(attrs={'placeholder': ugettext('Other Form of Name')}),
            'year_from': TextInput(attrs={'placeholder': ugettext('Year From')}),
            'year_to': TextInput(attrs={'placeholder': ugettext('Year To')}),
        }


class OtherNamesInline(InlineFormSet):
    extra = 1
    model = IsaarOtherName
    form_class = OtherNamesForm
    can_delete = True
    prefix = 'other_names'


class StandardizedNamesForm(ModelForm):
    class Meta:
        fields = ('name', 'standard')
        widgets = {
            'name': TextInput(attrs={'placeholder': ugettext('Standardized Form of Name')}),
            'standard': TextInput(attrs={'placeholder': ugettext('Standard')})
        }


class StandardizedNamesInline(InlineFormSet):
    extra = 1
    model = IsaarStandardizedName
    form_class = StandardizedNamesForm
    can_delete = True
    prefix = 'standardized_names'


class CorporateBodyIdentifiersForm(ModelForm):
    class Meta:
        fields = ('identifier', 'rule')
        widgets = {
            'identifier': TextInput(attrs={'placeholder': ugettext('Corporate Body Identifier')}),
            'rule': TextInput(attrs={'placeholder': ugettext('Rule')})
        }


class CorporateBodyIdentifiersInLine(InlineFormSet):
    extra = 1
    model = IsaarCorporateBodyIdentifier
    can_delete = True
    form_class = CorporateBodyIdentifiersForm
    prefix = 'corporate_body_identifiers'


class PlacesForm(ModelForm):
    qualifier = ModelChoiceField(queryset=IsaarPlaceQualifier.objects.all(),
                                 empty_label=ugettext('- Select Qualifier -'),
                                 required=False)

    class Meta:
        model = IsaarPlace
        fields = ('place', 'year_from', 'year_to')
        widgets = {
            'place': TextInput(attrs={'placeholder': ugettext('Place')}),
            'year_from': TextInput(attrs={'placeholder': ugettext('Year From')}),
            'year_to': TextInput(attrs={'placeholder': ugettext('Year To')}),
        }


class PlacesInline(InlineFormSet):
    extra = 1
    model = IsaarPlace
    form_class = PlacesForm
    can_delete = True
    prefix = 'places'