from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget


class CountrySelect2Widget(ModelSelect2Widget):
    search_fields = [
        'country__icontains',
    ]
    attrs={'placeholder': '-- Select Country --'}


class LanguagesSelect2Widget(ModelSelect2MultipleWidget):
    search_fields = [
        'language__icontains',
    ]
    attrs={'placeholder': '-- Select Languages --'}

