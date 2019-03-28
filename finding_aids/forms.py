from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, Form, ModelForm, Textarea, HiddenInput, TextInput, CharField, NumberInput, \
    Select, ChoiceField
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from extra_views import InlineFormSet

from archival_unit.models import ArchivalUnit
from archival_unit.widgets import ArchivalUnitSeriesContainersSelect2Widget
from authority.widgets import *

from controlled_list.models import Locale, PersonRole, CorporationRole, GeoRole, LanguageUsage, ExtentUnit, DateType
from controlled_list.widgets import PersonRoleSelect2Widget, GeoRoleSelect2Widget, KeywordSelect2MultipleWidget, \
    LanguageUsageSelect2Widget, ExtentUnitSelect2Widget, DateTypeSelect2Widget, CorporationRoleSelect2Widget
from finding_aids.models import FindingAidsEntity, FindingAidsEntityAssociatedPerson, \
    FindingAidsEntityAssociatedCorporation, FindingAidsEntityAssociatedCountry, FindingAidsEntityAssociatedPlace, \
    FindingAidsEntityExtent, FindingAidsEntityLanguage, FindingAidsEntityDate

IMG_FLAG = ' <span class="flag"></span>'


class FindingAidsArchivalUnitForm(Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FindingAidsArchivalUnitForm, self).__init__(*args, **kwargs)
        qs = user.user_profile.allowed_archival_units.all().order_by('fonds', 'subfonds', 'series')
        qs_subfonds = ArchivalUnit.objects.filter(children__in=qs, level='SF').order_by('fonds', 'subfonds', 'series')
        qs_fonds = ArchivalUnit.objects.filter(children__in=qs_subfonds, level='F').order_by('fonds',
                                                                                             'subfonds', 'series')
        # If User is restricted to a particular series
        if len(qs) > 0:
            self.fields['fonds'] = ModelChoiceField(
                queryset=ArchivalUnit.objects.all(),
                widget=ModelSelect2Widget(
                    queryset=qs_fonds,
                    search_fields=['title__icontains', 'reference_code__icontains'],
                )
            )
            self.fields['subfonds'] = ModelChoiceField(
                queryset=ArchivalUnit.objects.all(),
                widget=ModelSelect2Widget(
                    queryset=qs_subfonds,
                    search_fields=['title__icontains', 'reference_code__icontains'],
                    dependent_fields={'fonds': 'parent'}
                )
            )
            self.fields['series'] = ModelChoiceField(
                queryset=ArchivalUnit.objects.all(),
                widget=ModelSelect2Widget(
                    queryset=qs,
                    search_fields=['title__icontains', 'reference_code__icontains'],
                    dependent_fields={'subfonds': 'parent'}
                )
            )
        else:
            self.fields['fonds'] = ModelChoiceField(
                queryset=ArchivalUnit.objects.all(),
                label='Fonds',
                widget=ModelSelect2Widget(
                    queryset=ArchivalUnit.objects.filter(level='F').order_by('fonds', 'subfonds', 'series'),
                    search_fields=['title__icontains', 'reference_code__icontains'],
                )
            )
            self.fields['subfonds'] = ModelChoiceField(
                queryset=ArchivalUnit.objects.all(),
                widget=ModelSelect2Widget(
                    queryset=ArchivalUnit.objects.filter(level='SF').order_by('fonds', 'subfonds', 'series'),
                    search_fields=['title__icontains', 'reference_code__icontains'],
                    dependent_fields={'fonds': 'parent'}
                )
            )
            self.fields['series'] = ModelChoiceField(
                queryset=ArchivalUnit.objects.all(),
                widget=ArchivalUnitSeriesContainersSelect2Widget(
                    queryset=ArchivalUnit.objects.filter(level='S').order_by('fonds', 'subfonds', 'series'),
                    search_fields=['title__icontains', 'reference_code__icontains'],
                    dependent_fields={'subfonds': 'parent'}
                )
            )


class FindingAidsTemplateSelectForm(Form):
    template_select = ModelChoiceField(
        queryset=FindingAidsEntity.objects.filter(is_template=True),
        empty_label=None
    )

    def __init__(self, *args, **kwargs):
        archival_unit = kwargs.pop('archival_unit', None)
        super(FindingAidsTemplateSelectForm, self).__init__(*args, **kwargs)
        self.fields['template_select'].queryset = FindingAidsEntity.objects.filter(is_template=True,
                                                                                   archival_unit=archival_unit)


class FindingAidsBaseForm(ModelForm):
    original_locale = ModelChoiceField(empty_label=ugettext('- Select Original Locale -'),
                                       queryset=Locale.objects.all(), required=False)

    class Meta:
        model = FindingAidsEntity
        exclude = '__all__'
        labels = {
            'uuid': mark_safe(ugettext('UUID')),
            'legacy_id': mark_safe(ugettext('Legacy ID')),
            'folder_no': mark_safe(ugettext('Level 1 Number')),
            'level': mark_safe(ugettext('Folder/Item')),
            'title_original': mark_safe(ugettext('Title - Original Language') + IMG_FLAG),
            'contents_summary_original': mark_safe(ugettext('Contents Summary - Original Language') + IMG_FLAG),
            'language_statement_original': mark_safe(ugettext('Language Statement - Original Language') + IMG_FLAG),
            'physical_description_original': mark_safe(ugettext('Physical Description - Original Language') + IMG_FLAG),
            'spatial_coverage_country': ugettext('Spatial Coverage (Countries)'),
            'spatial_coverage_place': ugettext('Spatial Coverage (Places)'),
            'subject_person': ugettext('Subjects (People)'),
            'subject_corporation': ugettext('Subjects (Corporations)'),
            'subject_keyword': ugettext('Keywords'),
            'genre': ugettext('Form/Genre')
        }
        widgets = {
            'uuid': TextInput(attrs={'readonly': True}),
            'archival_reference_code': TextInput(attrs={'readonly': True}),
            'folder_no': NumberInput(attrs={'readonly': True}),
            'contents_summary': Textarea(attrs={'rows': 3}),
            'contents_summary_original': Textarea(attrs={'rows': 3}),
            'language_statement': Textarea(attrs={'rows': 3}),
            'language_statement_original': Textarea(attrs={'rows': 3}),
            'physical_condition': Textarea(attrs={'rows': 3}),
            'physical_description': Textarea(attrs={'rows': 3}),
            'physical_description_original': Textarea(attrs={'rows': 3}),
            'spatial_coverage_country': CountrySelect2MultipleWidget(
                attrs={'data-placeholder': '-- Select Countries --'}),
            'spatial_coverage_place': PlaceSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Places --'}),
            'subject_person': PersonSelect2MultipleWidget(attrs={'data-placeholder': '-- Select People --'}),
            'subject_corporation': CorporationSelect2MultipleWidget(
                attrs={'data-placeholder': '-- Select Corporations --'}),
            'subject_keyword': KeywordSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Keywords --'}),
            'genre': GenreSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Genres --'}),
            'internal_note': Textarea(attrs={'rows': 3}),
            'duration': TextInput(attrs={'readonly': True}),
        }
        help_texts = {
            'date_from': 'Date format: YYYY, or YYYY-MM, or YYYY-MM-DD',
            'date_to': 'Date format: YYYY, or YYYY-MM, or YYYY-MM-DD',
            'time_start': 'Format: hh:mm:ss',
            'time_end': 'Format: hh:mm:ss'
        }


class FindingAidsForm(FindingAidsBaseForm):
    description_level_hidden = CharField(widget=HiddenInput(), required=False)

    class Meta(FindingAidsBaseForm.Meta):
        exclude = ['archival_unit', 'container', 'published', 'user_published', 'date_published',
                   'user_created', 'date_created', 'user_updated', 'date_updated', 'old_id', 'catalog_id']

    def clean_title(self):
        if not self.cleaned_data['title']:
            raise ValidationError(ugettext("This field is mandatory."))
        return self.cleaned_data['title']

    def clean_date_from(self):
        if not self.cleaned_data['date_from']:
            raise ValidationError(ugettext("This field is mandatory."))
        return self.cleaned_data['date_from']


class FindingAidsTemplateForm(FindingAidsBaseForm):
    class Meta(FindingAidsBaseForm.Meta):
        exclude = ['archival_unit', 'container', 'folder_no', 'archival_reference_code', 'level',
                   'description_level']

    def clean_template_name(self):
        if not self.cleaned_data['template_name']:
            raise ValidationError(ugettext("This field is mandatory."))
        return self.cleaned_data['template_name']


class FindingAidsUpdateForm(FindingAidsBaseForm):
    description_level = ChoiceField(required=False, choices=FindingAidsEntity.DESCRIPTION_LEVEL,
                                    widget=Select(attrs={'disabled': True}))

    level = ChoiceField(required=False, choices=FindingAidsEntity.FINDING_AIDS_LEVEL,
                        widget=Select(attrs={'disabled': True}))

    class Meta(FindingAidsBaseForm.Meta):
        exclude = ['archival_unit', 'container', 'published', 'user_published', 'date_published',
                   'user_created', 'date_created', 'user_updated', 'date_updated', 'old_id', 'catalog_id']

    def clean_title(self):
        if not self.cleaned_data['title']:
            raise ValidationError(ugettext("This field is mandatory."))
        return self.cleaned_data['title']

    def clean_date_from(self):
        if not self.cleaned_data['date_from']:
            raise ValidationError(ugettext("This field is mandatory."))
        return self.cleaned_data['date_from']


class FindingAidsTemplateUpdateForm(FindingAidsBaseForm):
    class Meta(FindingAidsBaseForm.Meta):
        exclude = ['archival_unit', 'container', 'folder_no', 'archival_reference_code', 'level',
                   'description_level']

    def clean_template_name(self):
        if not self.cleaned_data['template_name']:
            raise ValidationError(ugettext("This field is mandatory."))
        return self.cleaned_data['template_name']


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

    def has_changed(self):
        has_changed = ModelForm.has_changed(self)
        return bool(self.initial or has_changed)


class FindingAidsAssociatedPeopleInline(InlineFormSet):
    extra = 1
    model = FindingAidsEntityAssociatedPerson
    fields = '__all__'
    form_class = FindingAidsAssociatedPeopleForm
    can_delete = True
    prefix = 'associated_people'


class FindingAidsDateForm(ModelForm):
    date_type = ModelChoiceField(
        queryset=DateType.objects.all(),
        widget=DateTypeSelect2Widget(attrs={'data-placeholder': '-- Select Date Type --'}),
        required=False
    )

    def has_changed(self):
        has_changed = ModelForm.has_changed(self)
        return bool(self.initial or has_changed)


class FindingAidsDateInline(InlineFormSet):
    extra = 1
    model = FindingAidsEntityDate
    fields = '__all__'
    form_class = FindingAidsDateForm
    can_delete = True
    prefix = 'dates'


class FindingAidsAssociatedCorporationForm(ModelForm):
    associated_corporation = ModelChoiceField(
        queryset=Corporation.objects.all(),
        widget=CorporationSelect2Widget(attrs={'data-placeholder': '-- Select Corporation --'})
    )
    role = ModelChoiceField(
        queryset=CorporationRole.objects.all(),
        widget=CorporationRoleSelect2Widget(attrs={'data-placeholder': '-- Select Role --'}),
        required=False
    )

    def has_changed(self):
        has_changed = ModelForm.has_changed(self)
        return bool(self.initial or has_changed)


class FindingAidsAssociatedCorporationInline(InlineFormSet):
    extra = 1
    model = FindingAidsEntityAssociatedCorporation
    fields = '__all__'
    form_class = FindingAidsAssociatedCorporationForm
    can_delete = True
    prefix = 'associated_corporations'


class FindingAidsAssociatedCountryForm(ModelForm):
    associated_country = ModelChoiceField(
        queryset=Country.objects.all(),
        widget=CountrySelect2Widget(attrs={'data-placeholder': '-- Select Country --'})
    )
    role = ModelChoiceField(
        queryset=GeoRole.objects.all(),
        widget=GeoRoleSelect2Widget(attrs={'data-placeholder': '-- Select Role --'}),
        required=False
    )

    def has_changed(self):
        has_changed = ModelForm.has_changed(self)
        return bool(self.initial or has_changed)


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

    def has_changed(self):
        has_changed = ModelForm.has_changed(self)
        return bool(self.initial or has_changed)


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

    def has_changed(self):
        has_changed = ModelForm.has_changed(self)
        return bool(self.initial or has_changed)


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

    def has_changed(self):
        has_changed = ModelForm.has_changed(self)
        return bool(self.initial or has_changed)
    

class FindingAidsExtentInline(InlineFormSet):
    extra = 1
    model = FindingAidsEntityExtent
    fields = '__all__'
    form_class = FindingAidsExtentForm
    can_delete = True
    prefix = 'extents'
