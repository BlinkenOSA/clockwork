from django.forms import Form, ModelChoiceField, CharField
from django.utils.translation import ugettext
from archival_unit.models import ArchivalUnit
from archival_unit.widgets import ArchivalUnitSelect2Widget
from controlled_list.models import CarrierType, PrimaryType


class ContainerForm(Form):
    primary_type = ModelChoiceField(
        queryset=PrimaryType.objects.all(),
        empty_label=ugettext('- Choose Primary Type -')
    )
    carrier_type = ModelChoiceField(
        queryset=CarrierType.objects.all(),
        empty_label=ugettext('- Choose Carrier Type -')
    )
    container_label = CharField(max_length=100, required=False)
