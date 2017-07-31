from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget

from authority.models import Country, Language


class CountrySelect2Widget(ModelSelect2Widget):
    def get_search_fields(self):
        pass

    model = Country
    search_fields = [
        'country__icontains',
    ]
    attrs={'placeholder': '-- Select Country --'}


class LanguagesSelect2Widget(ModelSelect2MultipleWidget):
    def get_search_fields(self):
        pass

    model = Language
    search_fields = [
        'language__icontains',
    ]
    attrs={'placeholder': '-- Select Languages --'}

