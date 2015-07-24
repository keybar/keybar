import pytest

from keybar.tests.factories.device import (
    AuthorizedDeviceFactory, DeauthorizedDeviceFactory, DeviceFactory)


@pytest.mark.django_db
class TestDevice:

    def test_has_relation_to_user(self):
        device = DeviceFactory.create()
        assert device.user is not None

    def test_device_can_have_unknown_authorized_status(self):
        device = DeviceFactory.create()
        assert device.authorized is None

    def test_device_can_be_authorized(self):
        device = AuthorizedDeviceFactory.create()
        assert device.authorized is True

    def test_device_can_be_deauthorized(self):
        device = DeauthorizedDeviceFactory.create()
        assert device.authorized is False

    def test_fingerprint(self):
        expected = '550d 984c 174b ff11  ac45 3e5c 28b7 aa0b'

        device = DeviceFactory.create()
        assert device.fingerprint == expected
