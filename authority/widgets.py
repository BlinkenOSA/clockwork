from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget

from authority.models import Country, Language, Person, Genre


class CountrySelect2Widget(ModelSelect2Widget):
    model = Country
    search_fields = [
        'country__icontains',
    ]
    attrs={'placeholder': '-- Select Country --'}


class LanguagesSelect2Widget(ModelSelect2MultipleWidget):
    model = Language
    search_fields = [
        'language__icontains',
    ]
    attrs={'placeholder': '-- Select Languages --'}


class GenresSelect2Widget(ModelSelect2MultipleWidget):
    model = Genre
    search_fields = [
        'genre__icontains',
    ]
    attrs={'placeholder': '-- Select Genres --'}


class PersonSelect2Widget(ModelSelect2Widget):
    model = Person
    search_fields = [
        'first_name__icontains', 'last_name__icontains',
    ]
    attrs={'placeholder': '-- Select Person --'}

