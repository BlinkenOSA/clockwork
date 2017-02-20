from django_select2.forms import ModelSelect2Widget


class ArchivalUnitSelect2Widget(ModelSelect2Widget):
    search_fields = [
        'title__icontains', 'reference_code__icontains'
    ]
    attrs = {'placeholder': '-- Select Archival Unit --'}

    def label_from_instance(self, obj):
        return obj.title_full
