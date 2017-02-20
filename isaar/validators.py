from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_type(value):
    if value not in ['P', 'C', 'F']:
        raise ValidationError(
            _("%(value) should be either 'Person', 'Corporation', 'Family'"),
            params={'value': value},
        )


def validate_status(value):
    if value not in ['Final', 'Draft']:
        raise ValidationError(
            _("%(value) should be either 'Final' or 'Draft'")

        )
