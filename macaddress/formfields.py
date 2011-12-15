from django.forms import Field, util
from django.forms.fields import EMPTY_VALUES

from netaddr import EUI, AddrFormatError


class MACAddressField(Field):
    default_error_messages = {
        'invalid': 'Enter a valid MAC Address.',
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
            value = EUI(str(value))
        except (ValueError, TypeError, AddrFormatError):
            raise util.ValidationError(self.error_messages['invalid'])
        return value


