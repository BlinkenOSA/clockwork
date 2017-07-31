from django_select2.forms import ModelSelect2MultipleWidget

from isaar.models import Isaar


class IsaarRecordsSelect2Widget(ModelSelect2MultipleWidget):
    def get_search_fields(self):
        pass

    model = Isaar
    search_fields = [
        'name__icontains',
    ]
    attrs={'placeholder': '-- Select ISAAR/CPF Records --'}

