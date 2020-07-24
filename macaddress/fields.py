import django
from django.core.exceptions import ValidationError
from django.db import models

from netaddr import EUI, AddrFormatError

from .formfields import MACAddressField as MACAddressFormField

from . import default_dialect, format_mac, mac_linux

import warnings

class MACAddressField(models.Field):
    description = "A MAC address validated by netaddr.EUI"
    empty_strings_allowed = False
    dialect = None

    def __init__(self, *args, **kwargs):
        self.integer = kwargs.pop('integer', True)
        if not self.integer: # If storing MAC address as string, set max_length to default (17) or use supplied kwarg value.
            kwargs['max_length'] = kwargs.get('max_length', 17)
        super(MACAddressField, self).__init__(*args, **kwargs)


    def deconstruct(self):
        ''' Django 1.7 migrations require this method
            https://docs.djangoproject.com/en/dev/howto/custom-model-fields/#field-deconstruction
        '''
        name, path, args, kwargs = super(MACAddressField, self).deconstruct()
        kwargs['integer'] = self.integer
        return name, path, args, kwargs

    @classmethod
    def set_dialect(cls, new_dialect_clazz):
        ''' Setting dialect for EUI (MAC addresses) globally to this Field
        class.
        Class new_dialect_clazz should (finally) extend
        netaddr.strategy.eui48.mac_eui48.
        '''
        warnings.warn(
            "The set_dialect method has been deprecated, in favor of the default_dialect utility function and "
            " settings.MACADDRESS_DEFAULT_DIALECT. See macaddress.__init__.py source or the project README for "
            "more information.",
            DeprecationWarning,
        )
        cls.dialect = new_dialect_clazz

    def get_prep_value(self, value):
        if value is None:
            return None
        if not isinstance(value, EUI):
            value = self.to_python(value)
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

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, EUI):
            value.dialect = default_dialect(value)
            return value
        try:
            return EUI(value, version=48, dialect=default_dialect())
        except (TypeError, ValueError, AddrFormatError):
            raise ValidationError("This value must be a valid MAC address.")

    def formfield(self, **kwargs):
        defaults = {'form_class': MACAddressFormField}
        defaults.update(kwargs)
        return super(MACAddressField, self).formfield(**defaults)

    def get_prep_lookup(self, lookup_type, value):
        # data is stored internally as integer so searching as string
        # yield 0 result. for example: useful for search in admin.
        if lookup_type in ('exact', 'iexact', 'icontains', 'icontains'):
            try:
                return self.get_prep_value(value)
            except AddrFormatError:
                return None
        elif lookup_type in ('in'):
            try:
                macs = []
                for mac in value:
                    macs += [self.get_prep_value(mac)]
                return macs
            except AddrFormatError:
                return None
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)
