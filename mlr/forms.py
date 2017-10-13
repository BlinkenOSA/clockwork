from django.forms import ModelForm, ModelChoiceField
from django.utils.translation import ugettext

from controlled_list.models import Building
from mlr.models import MLREntity


class MLRForm(ModelForm):
    building = ModelChoiceField(queryset=Building.objects.all(),
                                empty_label=ugettext('- Select Building -'))

    class Meta:
        model = MLREntity
        exclude = ['series', 'carrier_type']