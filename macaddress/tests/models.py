"""
A model for testing
"""
from django.db import models
from macaddress.fields import MACAddressField

class NetworkThingy(models.Model):
    mac = MACAddressField()

    def __unicode__(self):
        return "%s" % self.mac
