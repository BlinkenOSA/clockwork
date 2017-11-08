from django.forms import ModelForm, ModelChoiceField, Form
from django.utils.translation import ugettext

from archival_unit.models import ArchivalUnit
from archival_unit.widgets import ArchivalUnitFondsSelect2Widget
from controlled_list.models import Building
from mlr.models import MLREntity


class MLRListForm(Form):
    fonds = ModelChoiceField(
        queryset=ArchivalUnit.objects.filter(level='F'),
        widget=ArchivalUnitFondsSelect2Widget(
            queryset=ArchivalUnit.objects.filter(level='F'),
        )
    )


class MLRForm(ModelForm):
    building = ModelChoiceField(queryset=Building.objects.all(),
                                empty_label=ugettext('- Select Building -'))

    class Meta:
        model = MLREntity
        exclude = ['series', 'carrier_type']