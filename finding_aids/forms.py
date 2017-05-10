from django.forms import ModelChoiceField, Form, CharField, ModelForm, ChoiceField, RadioSelect, HiddenInput, \
    TextInput, Select, IntegerField, Textarea
from django.utils.translation import ugettext

from archival_unit.models import ArchivalUnit
from archival_unit.widgets import ArchivalUnitSelect2Widget
from django_date_extensions.fields import ApproximateDateFormField

from controlled_list.models import Locale
from finding_aids.models import FindingAidsEntity


class FindingAidsArchivalUnitForm(Form):
    archival_unit = ModelChoiceField(
        queryset=ArchivalUnit.objects.filter(level='S').order_by('fonds', 'subfonds', 'series'),
        widget=ArchivalUnitSelect2Widget()
    )


class FindingAidsInContainerForm(ModelForm):
    container_name = CharField(required=False, widget=TextInput(attrs={'readonly': True}))
    item_no = CharField(required=True, label=ugettext('Item Number'), widget=TextInput(attrs={'readonly': True}))

    title = CharField(max_length=300, required=True)
    title_original = CharField(max_length=300, required=False)

    date_from = ApproximateDateFormField(required=True)
    date_to = ApproximateDateFormField(required=False)

    original_locale = ModelChoiceField(queryset=Locale.objects.all(), required=False)

    class Meta:
        model = FindingAidsEntity
        exclude = ['container']
        widgets = {
          'contents_summary': Textarea(attrs={'rows': 5}),
          'contents_summary_original': Textarea(attrs={'rows': 5}),
        }


class FindingAidsInContainerCreateForm(FindingAidsInContainerForm):
    FINDING_AIDS_LEVEL = [('F', 'Add Folder'), ('I', 'Add Item to Folder')]

    level = ChoiceField(choices=FINDING_AIDS_LEVEL, initial="F", label=ugettext('Action'))
    folder_no = ChoiceField(required=False, label=ugettext('Folder Number'))

    def __init__(self, *args, **kwargs):
        super(FindingAidsInContainerCreateForm, self).__init__(*args, **kwargs)
        self.fields['item_no'].initial = 0


class FindingAidsInContainerUpdateForm(FindingAidsInContainerForm):
    FINDING_AIDS_LEVEL = [('F', 'Update Folder'), ('I', 'Update Item in Folder')]

    level = ChoiceField(choices=FINDING_AIDS_LEVEL, initial="F")
    folder_no = ChoiceField(required=False, label=ugettext('Folder Number'), widget=Select(attrs={'readonly': True}))

    def clean_folder_no(self):
        return self.instance.folder_no
