from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_level(value):
    if value not in ['F', 'SF', 'S']:
        raise ValidationError(
            _("%(value) should be either 'Fonds', 'Subfonds', 'Series'"),
            params={'value': value},
        )


def validate_status(value):
    if value not in ['Final', 'Draft']:
        raise ValidationError(
            _("%(value) should be either 'Final' or 'Draft'")

        )
