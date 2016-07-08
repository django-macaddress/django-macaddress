django-macaddress
================

.. image:: https://api.travis-ci.org/django-macaddress/django-macaddress.png?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/django-macaddress/django-macaddress
.. image:: https://pypip.in/v/django-macaddress/badge.png
   :target: https://crate.io/packages/django-macaddress
.. image:: https://pypip.in/d/django-macaddress/badge.png
   :target: https://crate.io/packages/django-macaddress

MAC Address model and form fields for Django

We use netaddr to parse and validate the MAC address.  The tests aren't
complete yet.

Patches welcome: http://github.com/django-macaddress/django-macaddress

Release Notes:
**************

For release info: https://github.com/django-macaddress/django-macaddress/releases


Getting Started
***************

settings.MACADDRESS_DEFAULT_DIALECT
-----------------------------------
To specify a default dialect for presentation (and storage, see below), specify::
    
    settings.MACADDRESS_DEFAULT_DIALECT = 'module.dialect_class'

where the specified value is a string composed of a parent python module name 
and the child dialect class name. For example::

    settings.MACADDRESS_DEFAULT_DIALECT = 'netaddr.mac_eui48'

PS: old default of macaddress.mac_linux (uppercase and divided by ':' ) will be used by default.

If the custom dialect is defined in a package module, you will need to define the 
class in or import into the package's ``__init__.py``.

``default_dialect`` and ``format_mac``
--------------------------------------
To get the default dialect for your project, import and call the ``default_dialect`` function::

    >>> from macaddress import default_dialect
    
    >>> dialect = default_dialect()
    
This function may, optionally, be called with an ``netaddr.EUI`` class instance as its argument. If no
default is defined in ``settings``, it will return the dialect of the provided ``EUI`` object.

The ``format_mac`` function takes an ``EUI`` instance and a dialect class (``netaddr.mac_eui48`` or a 
subclass) as its arguments. The dialect class may be specified as a string in the same manner as 
``settings.MACADDRESS_DEFAULT_DIALECT``::
    
    >>> from netaddr import EUI, mac_bare
    >>> from macaddress import format_mac

    >>> mac = EUI('00:12:3c:37:64:8f')
    >>> format_mac(mac, mac_bare)
    '00123C37648F'
    >>> format_mac(mac, 'netaddr.mac_cisco')
    '0012.3c37.648f'
    
MACAddressField (ModelField)
----------------------------
This is an example model using MACAddressField::
    
    from macaddress.fields import MACAddressField
    
    class Computer(models.Model):
        name = models.CharField(max_length=32)
        eth0 = MACAddressField(null=True, blank=True)
        ...
    
The default behavior is to store the MAC Address in the database is a BigInteger. 
If you would, rather, store the value as a string (to, for instance, facilitate 
sub-string searches), you can specify ``integer=False`` and the value will be stored
as a string::

    class Computer(models.Model):
        name = models.CharField(max_length=32)
        eth0 = MACAddressField(blank=True, integer=False)
        ...

If you want to set ``unique=True`` on a MACAddressField that is stored as a string, you will need 
to set ``null=True`` and create custom ``clean_<foo>`` methods on your ``forms.ModelForm`` class for 
each MACAddressField that return ``None`` when the value provided is an ``''`` (empty string)::

    from .models import Computer
    
    class ComputerForm(forms.ModelForm):
        class Meta:
            model = Computer
        
        def clean_eth0(self):
            return self.cleaned_data['eth0'] or None
        
You should avoid changing the value of ``integer`` after running ``managy.py syncdb``, 
unless you are using a schema migration solution like South or Django's built-in migrations.


To Do
*****

+ Add greater support for partial string queries when storing MACs as strings in the database.
+ Add custom validator to check for duplicate MACs when mixing string and integer storage types.
+ Add deprecation warning and timeline for changeover to default string storage.
