from django_select2.forms import ModelSelect2Widget

from donor.models import Donor


class DonorSelect2Widget(ModelSelect2Widget):
    model = Donor
    search_fields = [
        'name__icontains',
    ]
    attrs={'placeholder': '-- Select Donor Records --'}

