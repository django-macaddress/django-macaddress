from django.conf import settings

from netaddr import mac_unix, mac_eui48

import importlib
import warnings

class mac_linux(mac_unix):
    """MAC format with zero-padded all upper-case hex and colon separated"""
    word_fmt = '%.2X'

def default_dialect(eui_obj=None):
    # Check to see if a default dialect class has been specified in settings,
    # using 'module.dialect_cls' string and use importlib and getattr to retrieve dialect class. 'module' is the module and
    # 'dialect_cls' is the class name of the custom dialect. The dialect must either be defined or imported by the module's
    # __init__.py if the module is a package.
    from .fields import MACAddressField # Remove import at v1.4
    if hasattr(settings, 'MACADDRESS_DEFAULT_DIALECT') and not MACAddressField.dialect:
        module, dialect_cls = settings.MACADDRESS_DEFAULT_DIALECT.split('.')
        dialect = getattr(importlib.import_module(module), dialect_cls, mac_linux)
        return dialect
    else:
        if MACAddressField.dialect: # Remove this "if" statement at v1.4
            warnings.warn(
                "The set_dialect class method on MACAddressField has been deprecated, in favor of the default_dialect "
                "utility function and settings.MACADDRESS_DEFAULT_DIALECT. See macaddress.__init__.py source or the "
                "project README for more information.",
                DeprecationWarning,
            )
            return MACAddressField.dialect
        if eui_obj:
            return eui_obj.dialect
        else:
            return mac_linux

def format_mac(eui_obj, dialect):
    # Format a EUI instance as a string using the supplied dialect class, allowing custom string classes by
    # passing directly or as a string, a la 'module.dialect_cls', where 'module' is the module and 'dialect_cls'
    # is the class name of the custom dialect. The dialect must either be defined or imported by the module's __init__.py if
    # the module is a package.
    if not isinstance(dialect, mac_eui48):
        if isinstance(dialect, str):
            module, dialect_cls = dialect.split('.')
            dialect = getattr(importlib.import_module(module), dialect_cls)
    eui_obj.dialect = dialect
    return str(eui_obj)


from pkg_resources import get_distribution, DistributionNotFound
import os.path

try:
    _dist = get_distribution('django-macaddress')
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version
VERSION = __version__   # synonym
