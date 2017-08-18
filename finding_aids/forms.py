from django.forms import ModelChoiceField, Form, ModelForm, Textarea
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from extra_views import InlineFormSet

from archival_unit.models import ArchivalUnit
from authority.widgets import *

from controlled_list.models import Locale, PersonRole, CorporationRole, GeoRole
from controlled_list.widgets import PersonRoleSelect2Widget, GeoRoleSelect2Widget, KeywordSelect2MultipleWidget
from finding_aids.models import FindingAidsEntity, FindingAidsEntityAssociatedPerson, \
    FindingAidsEntityAssociatedCorporation, FindingAidsEntityAssociatedCountry, FindingAidsEntityAssociatedPlace

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

    class Meta:
        model = FindingAidsEntity
        fields = '__all__'
        labels = {
            'title_original': mark_safe(ugettext('Title - Original Language') + IMG_FLAG),
            'contents_summary_original': mark_safe(ugettext('Contents Summary - Original Language') + IMG_FLAG),
            'spatial_coverage_country': ugettext('Spatial Coverage (Countries)'),
            'spatial_coverage_place': ugettext('Spatial Coverage (Places)'),
            'subject_person': ugettext('Subject (People)'),
            'subject_corporation': ugettext('Subject (Corporations)'),
            'subject_keyword': ugettext('Keywords'),
            'genre': ugettext('Form/Genre')
        }
        widgets = {
            'contents_summary': Textarea(attrs={'rows': 3}),
            'contents_summary_original': Textarea(attrs={'rows': 3}),
            'spatial_coverage_country': CountrySelect2MultipleWidget(attrs={'data-placeholder': '-- Select Countries --'}),
            'spatial_coverage_place': PlaceSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Places --'}),
            'subject_person': PersonSelect2MultipleWidget(attrs={'data-placeholder': '-- Select People --'}),
            'subject_corporation': CorporationSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Corporations --'}),
            'subject_keyword': KeywordSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Keywords --'}),
            'genre': GenreSelect2MultipleWidget(attrs={'data-placeholder': '-- Select Genres --'})
        }
        help_texts = {
            'date_from': 'Date format: YYYY, or YYYY-MM, or YYYY-MM-DD',
            'date_to': 'Date format: YYYY, or YYYY-MM, or YYYY-MM-DD'
        }


class FindingAidsAssociatedPeopleForm(ModelForm):
    associated_person = ModelChoiceField(
        queryset=Person.objects.all(),
        widget=PersonSelect2Widget(attrs={'data-placeholder': '-- Select Person --'})
    )
    role = ModelChoiceField(
        queryset=PersonRole.objects.all(),
        widget=PersonRoleSelect2Widget(attrs={'data-placeholder': '-- Select Role --'})
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
        widget=CorporationSelect2Widget(attrs={'data-placeholder': '-- Select Role --'})
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
        widget=GeoRoleSelect2Widget(attrs={'data-placeholder': '-- Select Role --'})
    )


class FindingAidsAssociatedCountryInline(InlineFormSet):
    extra = 1
    model = FindingAidsEntityAssociatedCountry
    fields = '__all__'
    form_class = FindingAidsAssociatedCountryForm
    can_delete = True
    prefix = 'associated_countries'


class FindingAidsAssociatedPlaceForm(ModelForm):
    place = ModelChoiceField(
        queryset=Place.objects.all(),
        widget=PlaceSelect2Widget(attrs={'data-placeholder': '-- Select Place --'})
    )
    role = ModelChoiceField(
        queryset=GeoRole.objects.all(),
        widget=GeoRoleSelect2Widget(attrs={'data-placeholder': '-- Select Role --'})
    )


class FindingAidsAssociatedPlaceInline(InlineFormSet):
    extra = 1
    model = FindingAidsEntityAssociatedPlace
    fields = '__all__'
    form_class = FindingAidsAssociatedPlaceForm
    can_delete = True
    prefix = 'associated_places'

