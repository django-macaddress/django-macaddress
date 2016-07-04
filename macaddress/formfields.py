from django.forms import Field
from django.forms.fields import EMPTY_VALUES
#"From Django 1.8: The django.forms.util module has been renamed. Use django.forms.utils instead."
try:
    from django.forms.utils import ValidationError
except ImportError:
    from django.forms.util import ValidationError

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
            value = EUI(str(value), version=48)
        except (ValueError, TypeError, AddrFormatError):
            raise ValidationError(self.error_messages['invalid'])
        return value


