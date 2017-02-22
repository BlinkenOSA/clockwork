from django import forms
from django.db.models import Q
from django.forms import ModelForm, TextInput, HiddenInput
from accession.widgets import AccessionsSelect2Widget
from archival_unit.models import ArchivalUnit


class BaseModelForm(ModelForm):
    class Meta:
        model = ArchivalUnit
        fields = ("fonds", "subfonds", "series", "parent", "level", "title", "acronym", "accession")


class FondsCreateForm(BaseModelForm):
    class Meta(BaseModelForm.Meta):
        widgets = {
            'parent': HiddenInput(),
            'level': HiddenInput(),
            'subfonds': HiddenInput(),
            'series': HiddenInput(),
            'accession': AccessionsSelect2Widget()
        }


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
        widgets = {
            'parent': HiddenInput(),
            'level': HiddenInput(),
            'fonds': TextInput(attrs={'readonly': True}),
            'series': HiddenInput(),
            'accession': AccessionsSelect2Widget()
        }


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
        widgets = {
            'parent': HiddenInput(),
            'level': HiddenInput(),
            'fonds': TextInput(attrs={'readonly': True}),
            'subfonds': TextInput(attrs={'readonly': True}),
            'accession': AccessionsSelect2Widget()
        }


class SeriesUpdateForm(SeriesCreateForm):
    class Meta(SeriesCreateForm.Meta):
        widgets = SeriesCreateForm.Meta.widgets