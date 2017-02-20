from django import forms
from django.forms import ModelForm, TextInput, HiddenInput, ModelChoiceField
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
    class Meta(FondsCreateForm.Meta):
        widgets = FondsCreateForm.Meta.widgets
        widgets.update({
            'fonds': TextInput(attrs={'readonly': True})
        })


class SubFondsCreateForm(BaseModelForm):
    fonds_title = forms.CharField(label='Fonds Title', required=False, widget=TextInput(attrs={'readonly': 'readonly'}))

    class Meta(BaseModelForm.Meta):
        widgets = {
            'parent': HiddenInput(),
            'level': HiddenInput(),
            'fonds': TextInput(attrs={'readonly': True}),
            'series': HiddenInput(),
            'accession': AccessionsSelect2Widget()
        }


class SubFondsUpdateForm(SubFondsCreateForm):
    class Meta(SubFondsCreateForm.Meta):
        widgets = SubFondsCreateForm.Meta.widgets
        widgets.update({
            'subfonds': TextInput(attrs={'readonly': True})
        })


class SeriesCreateForm(BaseModelForm):
    fonds_title = forms.CharField(label='Fonds Title', required=False, widget=TextInput(attrs={'readonly': 'readonly'}))
    subfonds_title = forms.CharField(label='Subfonds Title', required=False, widget=TextInput(attrs={'readonly': 'readonly'}))

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
        widgets.update({
            'series': TextInput(attrs={'readonly': True})
        })