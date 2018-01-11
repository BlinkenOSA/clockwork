from django.forms import ModelForm, ModelChoiceField, Form, CharField, TextInput
from django.utils.translation import ugettext
from extra_views import InlineFormSet

from archival_unit.models import ArchivalUnit
from archival_unit.widgets import ArchivalUnitFondsSelect2Widget
from controlled_list.models import Building
from mlr.models import MLREntity, MLREntityLocation


class MLRListForm(Form):
    fonds = ModelChoiceField(
        queryset=ArchivalUnit.objects.filter(level='F'),
        widget=ArchivalUnitFondsSelect2Widget(
            queryset=ArchivalUnit.objects.filter(level='F'),
        )
    )


class MLRLocationForm(ModelForm):
    building = ModelChoiceField(queryset=Building.objects.all(),
                                empty_label=ugettext('- Select Building -'))

    class Meta:
        model = MLREntityLocation
        fields = '__all__'


class MLRLocationInline(InlineFormSet):
    extra = 1
    model = MLREntityLocation
    form = MLRLocationForm
    fields = '__all__'
    can_delete = True
    prefix = 'mlr_locations'


class MLRForm(ModelForm):
    series_name = CharField(required=False, widget=TextInput(attrs={'disabled': 'disabled'}),
                            label=ugettext('Series'))
    carrier_type_name = CharField(required=False, widget=TextInput(attrs={'disabled': 'disabled'}),
                                  label=ugettext('Carrier Type'))

    class Meta:
        model = MLREntity
        exclude = ['series', 'carrier_type']
