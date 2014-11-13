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
