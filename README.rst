django-macaddress
================

MAC Address model and form fields for Django

We use netaddr to parse and validate the MAC address.  The tests aren't
complete yet.

Patches welcome: http://github.com/tubaman/django-macaddress


Changing dialect for MAC Address representation
-----------------------------------------------

By default, our mac_linux representation for MAC Address is used.
You can use some other available in python (or even create a new one) by setting
it: ``MACAddressField.set_dialect(your_dialect_clazz)``.

For more on python's representation of MAC Addresses, check:
http://pythonhosted.org/netaddr/tutorial_02.html#formatting
