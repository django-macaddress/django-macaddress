import pytest
from django.core.exceptions import ValidationError
from django.db import transaction
from django.test import TestCase

from .models import NetworkThingy


class MACAddressFieldTestCase(TestCase):
    def test_insert_valid_macaddress(self):
        mac_example = "00:11:22:33:44:aa"
        x = NetworkThingy(mac=mac_example)
        x.save()
        qm = NetworkThingy.objects
        assert x.mac == mac_example
        assert qm.get(mac=mac_example).mac == mac_example
        assert qm.all().count() == 1

    def test_insert_invalid_macaddress(self):
        invalid_mac = "XX"
        with transaction.atomic():
            x = NetworkThingy()
            x.mac = invalid_mac
            with pytest.raises(ValidationError):
                x.save()
        assert NetworkThingy.objects.all().count() == 0
