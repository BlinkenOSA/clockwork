from django import forms
from django.forms import ModelMultipleChoiceField
from userena.forms import EditProfileForm
from userena.utils import get_profile_model

from archival_unit.models import ArchivalUnit


class UserProfileAdminForm(forms.ModelForm):
    allowed_archival_units = ModelMultipleChoiceField(queryset=ArchivalUnit.objects.filter(level='S'),
                                                      required=False)


class UserProfileEditForm(EditProfileForm):
    class Meta:
        model = get_profile_model()
        exclude = ['user', 'allowed_archival_units']