from django_select2.forms import ModelSelect2Widget


class DonorSelect2Widget(ModelSelect2Widget):
    search_fields = [
        'name__icontains',
    ]
    attrs={'placeholder': '-- Select Donor Records --'}

