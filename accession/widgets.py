from django_select2.forms import ModelSelect2MultipleWidget


class AccessionsSelect2Widget(ModelSelect2MultipleWidget):
    search_fields = [
        'title__icontains', 'seq__icontains',
    ]
    attrs={'placeholder': '-- Select Accession Record --'}


