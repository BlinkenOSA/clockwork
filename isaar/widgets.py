from django_select2.forms import ModelSelect2MultipleWidget


class IsaarRecordsSelect2Widget(ModelSelect2MultipleWidget):
    search_fields = [
        'name__icontains',
    ]
    attrs={'placeholder': '-- Select ISAAR/CPF Records --'}

