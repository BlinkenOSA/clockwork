from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm, TextInput, HiddenInput
from django.utils.translation import ugettext

from accession.widgets import AccessionsSelect2Widget
from archival_unit.models import ArchivalUnit
from controlled_list.widgets import ArchivalUnitThemeSelect2MultipleWidget


class BaseModelForm(ModelForm):
    class Meta:
        model = ArchivalUnit
        fields = ("fonds", "subfonds", "series", "title", "title_original", "original_locale", "acronym", "theme")

    def clean(self):
        if self.cleaned_data["title_original"] and not self.cleaned_data["original_locale"]:
            raise ValidationError({'original_locale': ugettext("Original langauge should be selected.")})


class FondsCreateForm(BaseModelForm):
    class Meta(BaseModelForm.Meta):
        labels = {
            'title_original': ugettext('Original Title'),
            'original_locale': ugettext('Locale')
        }
        widgets = {
            'subfonds': HiddenInput(),
            'series': HiddenInput(),
            'theme': ArchivalUnitThemeSelect2MultipleWidget()
        }

    def clean_fonds(self):
        fonds = self.cleaned_data['fonds']
        if fonds <= 0:
            raise ValidationError(ugettext("Should be not less than 0."))
        else:
            return fonds

    def clean(self):
        super(FondsCreateForm, self).clean()
        f = ArchivalUnit.objects.filter(fonds=self.cleaned_data['fonds'],
                                        subfonds=self.cleaned_data['subfonds'],
                                        series=self.cleaned_data['series'],
                                        level="F")
        if len(f) > 0:
            raise ValidationError({'series': ugettext("Fonds with this number already exists!")})


class FondsUpdateForm(FondsCreateForm):
    def save(self, commit=True, *args, **kwargs):
        if 'fonds' in self.changed_data:
            fonds_orig = ArchivalUnit.objects.get(pk=self.instance.pk).fonds
            fonds_new = self.cleaned_data['fonds']
            archival_units = ArchivalUnit.objects.filter(Q(level='S') | Q(level='SF'), fonds=fonds_orig)
            for archival_unit in archival_units:
                archival_unit.fonds = fonds_new
                archival_unit.save()
        return super(FondsUpdateForm, self).save(commit=True)


class SubFondsCreateForm(BaseModelForm):
    fonds_title = forms.CharField(label='Fonds Title', required=False, widget=TextInput(attrs={'readonly': 'readonly'}))
    fonds_acronym = forms.CharField(label='Fonds Acronym', required=False, widget=TextInput(attrs={'readonly': 'readonly'}))

    class Meta(BaseModelForm.Meta):
        labels = {
            'title_original': ugettext('Original Title'),
            'original_locale': ugettext('Locale')
        }
        widgets = {
            'fonds': TextInput(attrs={'readonly': True}),
            'series': HiddenInput(),
            'theme': ArchivalUnitThemeSelect2MultipleWidget()
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        subfonds = self.cleaned_data['subfonds']
        if not title:
            if subfonds != 0:
                raise ValidationError(ugettext("Title is mandatory."))
            else:
                return title
        else:
            return title

    def clean_subfonds(self):
        subfonds = self.cleaned_data['subfonds']
        if subfonds < 0:
            raise ValidationError(ugettext("Should be not less than 0."))
        else:
            return subfonds

    def clean(self):
        super(SubFondsCreateForm, self).clean()
        sf = ArchivalUnit.objects.filter(fonds=self.cleaned_data['fonds'],
                                         subfonds=self.cleaned_data['subfonds'],
                                         series=self.cleaned_data['series'],
                                         level="SF")
        if len(sf) > 0:
            raise ValidationError({'subfonds': ugettext("Subfonds with this number already exists!")})


class SubFondsUpdateForm(SubFondsCreateForm):
    def save(self, commit=True, *args, **kwargs):
        if 'subfonds' in self.changed_data:
            subfonds_orig = ArchivalUnit.objects.get(pk=self.instance.pk).subfonds
            subfonds_new = self.cleaned_data['subfonds']
            archival_units = ArchivalUnit.objects.filter(level='S', subfonds=subfonds_orig)
            for archival_unit in archival_units:
                archival_unit.subfonds = subfonds_new
                archival_unit.save()
        return super(SubFondsUpdateForm, self).save(commit=True)


class SeriesCreateForm(BaseModelForm):
    fonds_title = forms.CharField(label='Fonds Title', required=False, widget=TextInput(attrs={'readonly': 'readonly'}))
    fonds_acronym = forms.CharField(label='Fonds Acronym', required=False, widget=TextInput(attrs={'readonly': 'readonly'}))
    subfonds_title = forms.CharField(label='Subfonds Title', required=False, widget=TextInput(attrs={'readonly': 'readonly'}))
    subfonds_acronym = forms.CharField(label='Subfonds Acronym', required=False, widget=TextInput(attrs={'readonly': 'readonly'}))

    class Meta(BaseModelForm.Meta):
        labels = {
            'title_original': ugettext('Original Title'),
            'original_locale': ugettext('Locale')
        }
        widgets = {
            'fonds': TextInput(attrs={'readonly': True}),
            'subfonds': TextInput(attrs={'readonly': True}),
            'theme': ArchivalUnitThemeSelect2MultipleWidget()
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if not title:
            raise ValidationError(ugettext("Title is mandatory."))
        else:
            return title

    def clean_series(self):
        series = self.cleaned_data['series']
        if series <= 0:
            raise ValidationError(ugettext("Should be bigger than 0."))
        else:
            return series

    def clean(self):
        super(SeriesCreateForm, self).clean()
        s = ArchivalUnit.objects.filter(fonds=self.cleaned_data['fonds'],
                                         subfonds=self.cleaned_data['subfonds'],
                                         series=self.cleaned_data['series'],
                                         level="S")
        if len(s) > 0:
            raise ValidationError({'series': ugettext("Series with this number already exists!")})


class SeriesUpdateForm(SeriesCreateForm):
    class Meta(SeriesCreateForm.Meta):
        widgets = SeriesCreateForm.Meta.widgets