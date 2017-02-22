from django import forms
from django.forms import ModelForm, Select, ModelChoiceField
from django.utils.translation import ugettext

from authority.models import Country
from authority.widgets import CountrySelect2Widget
from donor.models import Donor


class DonorForm(ModelForm):
    class Meta:
        model = Donor
        fields = '__all__'
        widgets = {
            'country': CountrySelect2Widget
        }

    def clean(self):
        cleaned_data = super(DonorForm, self).clean()

        email = cleaned_data.get("email")
        website = cleaned_data.get("website")

        if email == "" and website == "":
            raise forms.ValidationError(
                {'email': ugettext("E-mail or Website information is needed."),
                 'website': ugettext("E-mail or Website information is needed.")}
            )