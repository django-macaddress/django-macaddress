from django.core.validators import EMPTY_VALUES
from django.forms import Field
from django.forms.utils import ValidationError
from django.utils.translation import ugettext_lazy as _

from netaddr import EUI, AddrFormatError


class MACAddressField(Field):
    default_error_messages = {
        'invalid': _('Enter a valid MAC Address.'),
    }

    def clean(self, value):
        """
        Validates that EUI() can be called on the input. Returns the result
        of EUI(). Returns None for empty values.
        """
        value = super(MACAddressField, self).clean(value)
        if value in EMPTY_VALUES:
            return None
        try:
            value = EUI(str(value), version=48)
        except (ValueError, TypeError, AddrFormatError):
            raise ValidationError(self.error_messages['invalid'])
        return value


