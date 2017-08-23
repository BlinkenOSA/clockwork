from django.db.models import TextField
from django.forms import ModelChoiceField, Form, ModelForm, Textarea, HiddenInput, TextInput, CharField, NumberInput, \
    Select, ChoiceField
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from extra_views import InlineFormSet

from archival_unit.models import ArchivalUnit
from authority.widgets import *

from controlled_list.models import Locale, PersonRole, CorporationRole, GeoRole, LanguageUsage, ExtentUnit
from controlled_list.widgets import PersonRoleSelect2Widget, GeoRoleSelect2Widget, KeywordSelect2MultipleWidget, \
    LanguageUsageSelect2Widget, ExtentUnitSelect2Widget
from finding_aids.models import FindingAidsEntity, FindingAidsEntityAssociatedPerson, \
    FindingAidsEntityAssociatedCorporation, FindingAidsEntityAssociatedCountry, FindingAidsEntityAssociatedPlace, \
    FindingAidsEntityExtent, FindingAidsEntityLanguage

IMG_FLAG = ' <span class="flag"></span>'


class FindingAidsArchivalUnitForm(Form):
    fonds = ModelChoiceField(
        queryset=ArchivalUnit.objects.all(),
        label='Fonds',
        widget=ModelSelect2Widget(
            queryset=ArchivalUnit.objects.filter(level='F'),
            search_fields=['title__icontains', 'reference_code__icontains'],
        )
    )
    subfonds = ModelChoiceField(
        queryset=ArchivalUnit.objects.all(),
        widget=ModelSelect2Widget(
            queryset=ArchivalUnit.objects.filter(level='SF').order_by('fonds', 'subfonds', 'series'),
            search_fields=['title__icontains', 'reference_code__icontains'],
            dependent_fields={'fonds': 'parent'}
        )
    )
    series = ModelChoiceField(
        queryset=ArchivalUnit.objects.all(),
        widget=ModelSelect2Widget(
            queryset=ArchivalUnit.objects.filter(level='S').order_by('fonds', 'subfonds', 'series'),
            search_fields=['title__icontains', 'reference_code__icontains'],
            dependent_fields={'subfonds': 'parent'}
        )
    )


class FindingAidsForm(ModelForm):
    original_locale = ModelChoiceField(empty_label=ugettext('- Select Original Locale -'),
                                       queryset=Locale.objects.all(), required=False)
    level_hidden = CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = FindingAidsEntity
        fields = '__all__'
        labels = {
            'uuid': mark_safe(ugettext('UUID')),
            'folder_no': mark_safe(ugettext('Folder Number (if applicable)')),
            'title_original': mark_safe(ugettext('Title - Original Language') + IMG_FLAG),
            'contents_summary_original': mark_safe(ugettext('Contents Summary - Original Language') + IMG_FLAG),
            'language_statement_original': mark_safe(ugettext('Language Statement - Original Language') + IMG_FLAG),
            'physical_description_original': mark_safe(ugettext('Physical Description - Original Language') + IMG_FLAG),
            'spatial_coverage_country': ugettext('Spatial Coverage (Countries)'),
            'spatial_coverage_place': ugettext('Spatial Coverage (Places)'),
            'subject_person': ugettext('Subject (People)'),
            'subject_corporation': ugettext('Subject (Corporations)'),
            'subject_keyword': ugettext('Keywords'),
            'genre': ugettext('Form/Genre')
        }
        widgets = {
            'uuid': TextInput(attrs={'readonly': True}),
            'archival_reference_code': TextInput(attrs={'readonly': True}),
            'folder_no': NumberInput(attrs={'readonly': True}),
            'container': HiddenInput(),
            'primary_type': HiddenInput(),
            'contents_summary': Textarea(attrs={'rows': 3}),
            'contents_summary_original': Textarea(attrs={'rows': 3}),
            'language_statement': Textarea(attrs={'rows': 3}),
            'language_statement_original': Textarea(attrs={'rows': 3}),
            'physical_condition': Textarea(attrs={'rows': 3}),
            'physical_description': Textarea(attrs={'rows': 3}),
            'physical_description_original': Textarea(attrs={'rows': 3}),
            'spatial_coverage_country': CountrySelect2MultipleWidget(attrs={'data-placeholder': '-- Select Countries --'}),
            'spatial_coverage_place': PlaceSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Places --'}),
            'subject_person': PersonSelect2MultipleWidget(attrs={'data-placeholder': '-- Select People --'}),
            'subject_corporation': CorporationSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Corporations --'}),
            'subject_keyword': KeywordSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Keywords --'}),
            'genre': GenreSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Genres --'}),
            'internal_note': Textarea(attrs={'rows': 3})
        }
        help_texts = {
            'date_from': 'Date format: YYYY, or YYYY-MM, or YYYY-MM-DD',
            'date_to': 'Date format: YYYY, or YYYY-MM, or YYYY-MM-DD',
            'time_start': 'Time format: hh:mm:ss',
            'time_end': 'Time format: hh:mm:ss'
        }


class FindingAidsUpdateForm(ModelForm):
    original_locale = ModelChoiceField(empty_label=ugettext('- Select Original Locale -'),
                                       queryset=Locale.objects.all(), required=False)
    level_hidden = CharField(widget=HiddenInput(), required=False)
    level = ChoiceField(required=False, choices=FindingAidsEntity.FINDING_AIDS_LEVEL, widget=Select(attrs={'disabled': True}))

    class Meta:
        model = FindingAidsEntity
        fields = '__all__'
        labels = {
            'uuid': mark_safe(ugettext('UUID')),
            'folder_no': mark_safe(ugettext('Folder Number (if applicable)')),
            'title_original': mark_safe(ugettext('Title - Original Language') + IMG_FLAG),
            'contents_summary_original': mark_safe(ugettext('Contents Summary - Original Language') + IMG_FLAG),
            'language_statement_original': mark_safe(ugettext('Language Statement - Original Language') + IMG_FLAG),
            'physical_description_original': mark_safe(ugettext('Physical Description - Original Language') + IMG_FLAG),
            'spatial_coverage_country': ugettext('Spatial Coverage (Countries)'),
            'spatial_coverage_place': ugettext('Spatial Coverage (Places)'),
            'subject_person': ugettext('Subject (People)'),
            'subject_corporation': ugettext('Subject (Corporations)'),
            'subject_keyword': ugettext('Keywords'),
            'genre': ugettext('Form/Genre')
        }
        widgets = {
            'uuid': TextInput(attrs={'readonly': True}),
            'archival_reference_code': TextInput(attrs={'readonly': True}),
            'folder_no': NumberInput(attrs={'readonly': True}),
            'container': HiddenInput(),
            'primary_type': HiddenInput(),
            'contents_summary': Textarea(attrs={'rows': 3}),
            'contents_summary_original': Textarea(attrs={'rows': 3}),
            'language_statement': Textarea(attrs={'rows': 3}),
            'language_statement_original': Textarea(attrs={'rows': 3}),
            'physical_condition': Textarea(attrs={'rows': 3}),
            'physical_description': Textarea(attrs={'rows': 3}),
            'physical_description_original': Textarea(attrs={'rows': 3}),
            'spatial_coverage_country': CountrySelect2MultipleWidget(attrs={'data-placeholder': '-- Select Countries --'}),
            'spatial_coverage_place': PlaceSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Places --'}),
            'subject_person': PersonSelect2MultipleWidget(attrs={'data-placeholder': '-- Select People --'}),
            'subject_corporation': CorporationSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Corporations --'}),
            'subject_keyword': KeywordSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Keywords --'}),
            'genre': GenreSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Genres --'}),
            'internal_note': Textarea(attrs={'rows': 3})
        }
        help_texts = {
            'date_from': 'Date format: YYYY, or YYYY-MM, or YYYY-MM-DD',
            'date_to': 'Date format: YYYY, or YYYY-MM, or YYYY-MM-DD',
            'time_start': 'Time format: hh:mm:ss',
            'time_end': 'Time format: hh:mm:ss'
        }


class FindingAidsAssociatedPeopleForm(ModelForm):
    associated_person = ModelChoiceField(
        queryset=Person.objects.all(),
        widget=PersonSelect2Widget(attrs={'data-placeholder': '-- Select Person --'})
    )
    role = ModelChoiceField(
        queryset=PersonRole.objects.all(),
        widget=PersonRoleSelect2Widget(attrs={'data-placeholder': '-- Select Role --'}),
        required=False
    )


class FindingAidsAssociatedPeopleInline(InlineFormSet):
    extra = 1
    model = FindingAidsEntityAssociatedPerson
    fields = '__all__'
    form_class = FindingAidsAssociatedPeopleForm
    can_delete = True
    prefix = 'associated_people'


class FindingAidsAssociatedCorporationForm(ModelForm):
    associated_corporation = ModelChoiceField(
        queryset=Corporation.objects.all(),
        widget=CorporationSelect2Widget(attrs={'data-placeholder': '-- Select Corporation --'})
    )
    role = ModelChoiceField(
        queryset=CorporationRole.objects.all(),
        widget=CorporationSelect2Widget(attrs={'data-placeholder': '-- Select Role --'}),
        required=False
    )


class FindingAidsAssociatedCorporationInline(InlineFormSet):
    extra = 1
    model = FindingAidsEntityAssociatedCorporation
    fields = '__all__'
    form_class = FindingAidsAssociatedCorporationForm
    can_delete = True
    prefix = 'associated_corporations'


class FindingAidsAssociatedCountryForm(ModelForm):
    country = ModelChoiceField(
        queryset=Country.objects.all(),
        widget=CountrySelect2Widget(attrs={'data-placeholder': '-- Select Country --'})
    )
    role = ModelChoiceField(
        queryset=GeoRole.objects.all(),
        widget=GeoRoleSelect2Widget(attrs={'data-placeholder': '-- Select Role --'}),
        required=False
    )


class FindingAidsAssociatedCountryInline(InlineFormSet):
    extra = 1
    model = FindingAidsEntityAssociatedCountry
    fields = '__all__'
    form_class = FindingAidsAssociatedCountryForm
    can_delete = True
    prefix = 'associated_countries'


class FindingAidsAssociatedPlaceForm(ModelForm):
    associated_place = ModelChoiceField(
        queryset=Place.objects.all(),
        widget=PlaceSelect2Widget(attrs={'data-placeholder': '-- Select Place --'})
    )
    role = ModelChoiceField(
        queryset=GeoRole.objects.all(),
        widget=GeoRoleSelect2Widget(attrs={'data-placeholder': '-- Select Role --'}),
        required=False
    )


class FindingAidsAssociatedPlaceInline(InlineFormSet):
    extra = 1
    model = FindingAidsEntityAssociatedPlace
    fields = '__all__'
    form_class = FindingAidsAssociatedPlaceForm
    can_delete = True
    prefix = 'associated_places'


class FindingAidsLanguageForm(ModelForm):
    language = ModelChoiceField(
        queryset=Language.objects.all(),
        widget=LanguageSelect2Widget(attrs={'data-placeholder': '-- Select Language --'})
    )
    language_usage = ModelChoiceField(
        queryset=LanguageUsage.objects.all(),
        widget=LanguageUsageSelect2Widget(attrs={'data-placeholder': '-- Select Language Usage --'}),
        required=False
    )


class FindingAidsLanguageInline(InlineFormSet):
    extra = 1
    model = FindingAidsEntityLanguage
    fields = '__all__'
    form_class = FindingAidsLanguageForm
    can_delete = True
    prefix = 'languages'


class FindingAidsExtentForm(ModelForm):
    extent_unit = ModelChoiceField(
        queryset=ExtentUnit.objects.all(),
        widget=ExtentUnitSelect2Widget(attrs={'data-placeholder': '-- Select Extent Unit --'})
    )


class FindingAidsExtentInline(InlineFormSet):
    extra = 1
    model = FindingAidsEntityExtent
    fields = '__all__'
    form_class = FindingAidsExtentForm
    can_delete = True
    prefix = 'extents'
