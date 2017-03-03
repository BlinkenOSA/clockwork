from django.forms import ModelChoiceField, Form, CharField, ModelForm, ChoiceField, RadioSelect, HiddenInput, \
    TextInput
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
    folder_no_select = ChoiceField(required=False, label=ugettext('Folder Number Select'))
    item_no_select = ChoiceField(required=False, label=ugettext('Item Number Select'))

    folder_no = CharField(label=ugettext('Folder Number'), widget=HiddenInput())
    item_no = CharField(label=ugettext('Item Number'), widget=HiddenInput())

    title = CharField(max_length=300, required=True)
    title_original = CharField(max_length=300)

    date_from = ApproximateDateFormField(required=True)
    date_to = ApproximateDateFormField(required=False)

    original_locale = ModelChoiceField(queryset=Locale.objects.all(), required=False)
    level = ChoiceField(choices=FindingAidsEntity.FINDING_AIDS_LEVEL, widget=RadioSelect(), initial="F")

    class Meta:
        model = FindingAidsEntity
        exclude = ['container']
