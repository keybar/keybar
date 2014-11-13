import pytest

from keybar.tests.factories.device import (
    DeviceFactory,
    AuthorizedDeviceFactory,
    DeauthorizedDeviceFactory)


@pytest.mark.django_db
class TestDevice:

    def test_has_relation_to_user(self):
        device = DeviceFactory.create()
        assert device.user is not None

    def test_device_requires_user_relation(self):
        with pytest.raises(ValueError):
            device = DeviceFactory.create(user=None)

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
        expected = '4b:74:c6:1d:c1:e2:14:30:e0:5c:cc:12:a0:63:04:92'

        device = DeviceFactory.create()
        assert device.fingerprint == expected