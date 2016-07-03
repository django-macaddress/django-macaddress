from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db import transaction

from netaddr.core import AddrFormatError

from .models import NetworkThingy


class MACAddressFieldTestCase(TestCase):

    def setUp(self):
        self.model = NetworkThingy

    def test_insert_valid_macaddress(self):
        mac_example = '00:11:22:33:44:AA'
        x = self.model()
        x.mac = mac_example
        x.save()
        self.assertEquals(x.mac, mac_example)
        self.assertEquals(NetworkThingy.objects.get(mac=mac_example).mac,
                mac_example)
        self.assertEquals(NetworkThingy.objects.all().count(), 1)

    def test_insert_invalid_macaddress(self):
        invalid_mac = 'XX'
        with transaction.atomic():
            x = self.model()
            with self.assertRaises(ValidationError):
                x.mac = invalid_mac
                x.save()
        self.assertEquals(NetworkThingy.objects.all().count(), 0)
