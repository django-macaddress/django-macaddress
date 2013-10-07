from django.core.exceptions import ValidationError
from django.db import models

from netaddr import EUI, AddrFormatError, mac_eui48

from formfields import MACAddressField as MACAddressFormField


class MACAddressField(models.Field):
    description = "A MAC address validated by netaddr.EUI"
    empty_strings_allowed = False
    __metaclass__ = models.SubfieldBase

    def get_prep_value(self, value):
        if value is None:
            return None
        if not isinstance(value, EUI):
            return int(EUI(value, dialect=mac_eui48))
        return int(value)

    def get_internal_type(self):
        return "BigIntegerField"

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, EUI):
            value.dialect = mac_eui48
            return value
        try:
            return EUI(value, dialect=mac_eui48)
        except (TypeError, ValueError, AddrFormatError):
            raise ValidationError(
                "This value must be a valid MAC address.")

    def formfield(self, **kwargs):
        defaults = {'form_class': MACAddressFormField}
        defaults.update(kwargs)
        return super(MACAddressField, self).formfield(**defaults)

    def get_prep_lookup(self, lookup_type, value):
        # data is stored internally as integer so searching as string
        # yeild 0 result. for example: useful for search in admin.
        if lookup_type in ('exact', 'iexact', 'icontains', 'icontains'):
            try:
                return self.get_prep_value(value)
            except AddrFormatError, e:
                raise TypeError('Lookup currently support only full & valid MACs')
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^macaddress\.fields\.MACAddressField"])
except ImportError:
    pass
