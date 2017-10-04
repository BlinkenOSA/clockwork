from django.core.exceptions import ValidationError
from django.forms import Form, ModelChoiceField, Select, Textarea, HiddenInput, ModelForm, BooleanField
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from extra_views import InlineFormSet

from archival_unit.models import ArchivalUnit
from archival_unit.widgets import ArchivalUnitIsadSelect2Widget
from authority.widgets import LanguageSelect2MultipleWidget
from controlled_list.models import AccessRight, ReproductionRight, RightsRestrictionReason, ExtentUnit, CarrierType, \
    Locale
from isaar.widgets import IsaarRecordsSelect2Widget
from isad.models import Isad, IsadCreator, IsadExtent, IsadCarrier, IsadRelatedFindingAids, IsadLocationOfOriginals, \
    IsadLocationOfCopies

ACCRUALS = (
    (True, 'Accruals expected.'),
    (False, 'No accruals expected'),
)

IMG_FLAG = ' <span class="flag"></span>'


class IsadArchivalUnitForm(Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(IsadArchivalUnitForm, self).__init__(*args, **kwargs)
        qs = user.user_profile.allowed_archival_units.all()
        # If User is restricted to a particular series
        if len(qs) > 0:
            self.fields['archival_unit'] = ModelChoiceField(
                queryset=ArchivalUnit.objects.all(),
                widget=ArchivalUnitIsadSelect2Widget(
                    queryset=qs
                )
            )
        else:
            self.fields['archival_unit'] = ModelChoiceField(
                queryset=ArchivalUnit.objects.all(),
                widget=ArchivalUnitIsadSelect2Widget(
                    queryset=ArchivalUnit.objects.filter(isad__isnull=True)
                )
            )


class IsadForm(ModelForm):
    access_rights = ModelChoiceField(queryset=AccessRight.objects.all(),
                                     empty_label=ugettext('- Choose Access Rights -'))
    reproduction_rights = ModelChoiceField(queryset=ReproductionRight.objects.all(),
                                           empty_label=ugettext('- Choose Reproduction Rights -'))
    rights_restriction_reason = ModelChoiceField(queryset=RightsRestrictionReason.objects.all(),
                                                 empty_label=ugettext('- Choose Restriction Reason -'))
    original_locale = ModelChoiceField(queryset=Locale.objects.all(), empty_label=ugettext('- Choose Language -'),
                                       label=ugettext('Original metadata language'), required=False)

    class Meta:
        model = Isad
        exclude = ['archival_unit']
        labels = {
            'year_from': ugettext('Date (From)'),
            'year_to': ugettext('Date (To)'),
            'isaar': ugettext('Creator (ISAAR)'),
            'date_predominant': ugettext('Predominant date'),
            'administrative_history': ugettext('Administrative / Biographical history'),
            'scope_and_content_abstract': ugettext('Scope and content (Abstract)'),
            'scope_and_content_narrative': ugettext('Scope and content (Narrative)'),
            'physical_characteristics': ugettext('Physical characteristics and technical requirements'),
            'rules_conventions': ugettext('Rules or conventions'),

            'administrative_history_original': mark_safe(ugettext('Administrative / Biographical history - Original language') + IMG_FLAG),
            'archival_history_original': mark_safe(ugettext('Archival history - Original language') + IMG_FLAG),
            'scope_and_content_abstract_original': mark_safe(ugettext('Scope and content (Abstract) - Original language') + IMG_FLAG),
            'scope_and_content_narrative_original': mark_safe(ugettext('Scope and content (Narrative) - Original language') + IMG_FLAG),
            'appraisal_original': mark_safe(ugettext('Appraisal - Original language') + IMG_FLAG),
            'system_of_arrangement_information_original': mark_safe(ugettext('System of Arrangement Information - Original language') + IMG_FLAG),
            'physical_characteristics_original': mark_safe(ugettext('Physical characteristics and technical requirements - Original language') + IMG_FLAG),
            'publication_note_original': mark_safe(ugettext('Publication note - Original language') + IMG_FLAG),
            'note_original': mark_safe(ugettext('Note - Original language') + IMG_FLAG),
            'internal_note_original': mark_safe(ugettext('Internal note - Original language') + IMG_FLAG),
            'archivists_note_original': mark_safe(ugettext('Archivists note - Original language') + IMG_FLAG)
        }
        help_texts = {
            'year_from': ugettext('Date format: YYYY'),
            'year_to': ugettext('Date format: YYYY'),
            'embargo': ugettext('Date format: YYYY, or YYYY-MM, or YYYY-MM-DD')
        }
        widgets = {
            'isaar': IsaarRecordsSelect2Widget(),
            'language': LanguageSelect2MultipleWidget(),
            'accruals': Select(choices=ACCRUALS),
            'scope_and_content_abstract': Textarea(attrs={'rows': 4}),
            'scope_and_content_narrative': Textarea(attrs={'rows': 4}),
            'appraisal': Textarea(attrs={'rows': 4}),
            'system_of_arrangement_information': Textarea(attrs={'rows': 4}),
            'physical_characteristics': Textarea(attrs={'rows': 4}),
            'publication_note': Textarea(attrs={'rows': 4}),
            'note': Textarea(attrs={'rows': 5}),
            'internal_note': Textarea(attrs={'rows': 5}),
            'archivists_note': Textarea(attrs={'rows': 5}),
            'rules_conventions': Textarea(attrs={'rows': 5}),

            'scope_and_content_abstract_original': Textarea(attrs={'rows': 4}),
            'scope_and_content_narrative_original': Textarea(attrs={'rows': 4}),
            'appraisal_original': Textarea(attrs={'rows': 4}),
            'system_of_arrangement_information_original': Textarea(attrs={'rows': 4}),
            'physical_characteristics_original': Textarea(attrs={'rows': 4}),
            'publication_note_original': Textarea(attrs={'rows': 4}),
            'note_original': Textarea(attrs={'rows': 5}),
            'internal_note_original': Textarea(attrs={'rows': 5}),
            'archivists_note_original': Textarea(attrs={'rows': 5}),
        }

    def clean(self):
        creator_not_exists = True
        isaar = self.cleaned_data["isaar"]
        creators_total = int(self.data["creators-TOTAL_FORMS"])
        for x in xrange(0, creators_total):
            creator = self.data["creators-" + str(x) + "-creator"]
            if creator != "":
                creator_not_exists = False
        if creator_not_exists and not isaar:
            raise ValidationError({'isaar': ugettext("Creator or Creator (ISAAR) should be selected.")})

        original_exists = False
        if self.cleaned_data["administrative_history_original"]:
            original_exists = True
        if self.cleaned_data["archival_history_original"]:
            original_exists = True
        if self.cleaned_data["scope_and_content_abstract_original"]:
            original_exists = True
        if self.cleaned_data["scope_and_content_narrative_original"]:
            original_exists = True
        if self.cleaned_data["appraisal_original"]:
            original_exists = True
        if self.cleaned_data["system_of_arrangement_information_original"]:
            original_exists = True
        if self.cleaned_data["physical_characteristics_original"]:
            original_exists = True
        if self.cleaned_data["note_original"]:
            original_exists = True
        if self.cleaned_data["internal_note_original"]:
            original_exists = True
        if self.cleaned_data["archivists_note_original"]:
            original_exists = True

        if original_exists and not self.cleaned_data["original_locale"]:
            raise ValidationError({'original_locale': ugettext("Original langauge should be selected.")})

        if self.has_changed():
            self.cleaned_data["approved"] = False


class IsadCreatorInline(InlineFormSet):
    extra = 1
    model = IsadCreator
    fields = '__all__'
    can_delete = True
    prefix = 'creators'


class IsadExtentForm(ModelForm):
    extent_unit = ModelChoiceField(queryset=ExtentUnit.objects.all(),
                                   empty_label=ugettext('- Select Extent Unit -'))

    class Meta:
        model = IsadExtent
        fields = '__all__'
        labels = {
            'approx': ugettext('Approx.')
        }


class IsadExtentInline(InlineFormSet):
    extra = 1
    model = IsadExtent
    form_class = IsadExtentForm
    can_delete = True
    prefix = 'extents'


class IsadCarrierForm(ModelForm):
    carrier_type = ModelChoiceField(queryset=CarrierType.objects.extra(select={'ord':'lower(type)'}).order_by('ord'),
                                    empty_label=ugettext('- Select Carrier -'))

    class Meta:
        model = IsadCarrier
        fields = '__all__'


class IsadCarrierInline(InlineFormSet):
    extra = 1
    model = IsadCarrier
    form_class = IsadCarrierForm
    can_delete = True
    prefix = 'carriers'


class IsadRelatedFindingAidsInline(InlineFormSet):
    extra = 1
    model = IsadRelatedFindingAids
    fields = '__all__'
    can_delete = True
    prefix = 'related_finding_aids'


class IsadLocationOfOriginalsInline(InlineFormSet):
    extra = 1
    model = IsadLocationOfOriginals
    fields = '__all__'
    can_delete = True
    prefix = 'location_of_originals'


class IsadLocationOfCopiesInline(InlineFormSet):
    extra = 1
    model = IsadLocationOfCopies
    fields = '__all__'
    can_delete = True
    prefix = 'location_of_copies'
