from django.forms import Form, ModelChoiceField, CharField, TextInput, ModelForm
from django.utils.translation import ugettext

from container.models import Container
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
    legacy_id = CharField(max_length=100, required=False, label='Legacy ID')
    container_label = CharField(max_length=100, required=False)


class ContainerUpdateForm(ModelForm):
    primary_type = ModelChoiceField(
        queryset=PrimaryType.objects.all(),
        empty_label=ugettext('- Choose Primary Type -')
    )
    carrier_type = ModelChoiceField(
        queryset=CarrierType.objects.all(),
        empty_label=ugettext('- Choose Carrier Type -')
    )
    permanent_id = CharField(max_length=100, required=False, widget=TextInput(attrs={'readonly': 'readonly'}))
    legacy_id = CharField(max_length=100, required=False, label='Legacy ID')
    container_no = CharField(max_length=100, required=False, widget=TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Container
        fields = ('container_no', 'primary_type', 'carrier_type', 'container_label')
