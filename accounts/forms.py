from django import forms
from django.forms import ModelMultipleChoiceField

from archival_unit.models import ArchivalUnit


class UserProfileAdminForm(forms.ModelForm):
    allowed_archival_units = ModelMultipleChoiceField(queryset=ArchivalUnit.objects.filter(level='S'),
                                                      required=False)