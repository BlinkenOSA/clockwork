from django.forms import ModelForm
from controlled_list.models import *


class AccessRightForm(ModelForm):
    class Meta:
        model = AccessRight
        fields = '__all__'


class ArchivalUnitThemeForm(ModelForm):
    class Meta:
        model = ArchivalUnitTheme
        fields = '__all__'


class BuildingForm(ModelForm):
    class Meta:
        model = Building
        fields = '__all__'


class CarrierTypeForm(ModelForm):
    class Meta:
        model = CarrierType
        fields = '__all__'


class CorporationRoleForm(ModelForm):
    class Meta:
        model = CorporationRole
        exclude = ['user_created', 'date_created', 'user_updated', 'date_updated']


class DateTypeForm(ModelForm):
    class Meta:
        model = DateType
        fields = '__all__'


class ExtentUnitForm(ModelForm):
    class Meta:
        model = ExtentUnit
        fields = '__all__'


class GeoRoleForm(ModelForm):
    class Meta:
        model = GeoRole
        exclude = ['user_created', 'date_created', 'user_updated', 'date_updated']


class KeywordForm(ModelForm):
    class Meta:
        model = Keyword
        exclude = ['user_created', 'date_created', 'user_updated', 'date_updated']


class LanguageUsageForm(ModelForm):
    class Meta:
        model = LanguageUsage
        fields = '__all__'


class LocaleForm(ModelForm):
    class Meta:
        model = Locale
        fields = '__all__'


class PersonRoleForm(ModelForm):
    class Meta:
        model = PersonRole
        exclude = ['user_created', 'date_created', 'user_updated', 'date_updated']


class PrimaryTypeForm(ModelForm):
    class Meta:
        model = PrimaryType
        fields = '__all__'


class ReproductionRightForm(ModelForm):
    class Meta:
        model = ReproductionRight
        fields = '__all__'


class RightsRestrictionReasonForm(ModelForm):
    class Meta:
        model = RightsRestrictionReason
        fields = '__all__'
