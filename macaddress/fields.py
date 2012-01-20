from django.core.exceptions import ValidationError
from django.db import models

from netaddr import EUI, AddrFormatError, mac_unix

from formfields import MACAddressField as MACAddressFormField

# monkey patch EUI to work around https://github.com/drkjam/netaddr/issues/21
# we need this if we use unique=True
def _eui_deepcopy(obj, memo=None):
    from copy import copy
    return copy(obj)
EUI.__deepcopy__ = _eui_deepcopy

class mac_linux(mac_unix):
    """MAC format with zero-padded all upper-case hex and colon separated"""
    word_fmt = '%.2X'


class MACAddressField(models.Field):
    description = "A MAC address validated by netaddr.EUI"
    empty_strings_allowed = False
    __metaclass__ = models.SubfieldBase

    def get_db_prep_value(self, value):
        if value is None:
            return None
        if not isinstance(value, EUI):
            return int(EUI(value, dialect=mac_linux))
        return int(value)

    def get_internal_type(self):
        return "BigIntegerField"

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, EUI):
            value.dialect = mac_linux
            return value
        try:
            return EUI(value, dialect=mac_linux)
        except (TypeError, ValueError, AddrFormatError):
            raise ValidationError(
                "This value must be a valid MAC address.")

    def formfield(self, **kwargs):
        defaults = {'form_class': MACAddressFormField}
        defaults.update(kwargs)
        return super(MACAddressField, self).formfield(**defaults)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^macaddress\.fields\.MACAddressField"])
except ImportError:
    pass
