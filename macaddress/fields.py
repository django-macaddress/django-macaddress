from django.core.exceptions import ValidationError
from django.db import models

from netaddr import EUI, AddrFormatError

from .formfields import MACAddressField as MACAddressFormField

from . import default_dialect, format_mac
                 
class MACAddressField(models.Field):
    description = "A MAC address validated by netaddr.EUI"
    empty_strings_allowed = False
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, integer=True, *args, **kwargs): # Custom __init__ to accept new "integer" boolean argument to support specification of string or integer storage. Defaults to True (for now).
        self.integer = integer
        if not self.integer: # If storing MAC address as string, set max_length to default (17) or use supplied kwarg value.
            kwargs['max_length'] = kwargs.get('max_length', 17)
        super(MACAddressField, self).__init__(*args, **kwargs)
    
    def get_prep_value(self, value):
        if value is None:
            return None
        if not isinstance(value, EUI):
            value = EUI(value, dialect=default_dialect())
            if self.integer:
                return int(value)
            return str(value)
        value.dialect = default_dialect(self)
        if self.integer:
            return int(value)
        return str(value)
    
    def get_internal_type(self):
        if self.integer:
            return 'BigIntegerField'
        return 'CharField'
            
    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, EUI):
            value.dialect = default_dialect(value)
            return value
        try:
            return EUI(value, dialect=default_dialect())
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
                return None
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^macaddress\.fields\.MACAddressField"])
except ImportError:
    pass
