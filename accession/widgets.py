from django_select2.forms import ModelSelect2MultipleWidget

from accession.models import Accession


class AccessionsSelect2Widget(ModelSelect2MultipleWidget):
    model = Accession
    search_fields = [
        'title__icontains', 'seq__icontains',
    ]
    attrs={'placeholder': '-- Select Accession Record --'}


