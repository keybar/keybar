import mock
import pytest

from keybar.client import TestClient
from keybar.models.device import Device
from keybar.tests.factories.device import PRIVATE_KEY, PUBLIC_KEY, AuthorizedDeviceFactory
from keybar.tests.factories.user import UserFactory
from keybar.utils.crypto import generate_rsa_keys


@pytest.mark.django_db(transaction=True)
class TestDevicesEndpoint:

    def test_register(self, keybar_liveserver):
        client = TestClient(keybar_liveserver)

        response = client.register_device(
            'Test Device',
            str(PUBLIC_KEY.exportKey('PEM'), 'ascii'))

        assert response.status_code == 200
        assert response.json() == {
            'name': 'Test Device',
            'id': mock.ANY,
            'authorized': None
        }

        assert Device.objects.get().user is None

    def test_list(self, settings, keybar_liveserver):
        user = UserFactory.create(is_superuser=True)
        device = AuthorizedDeviceFactory.create(user=user)

        # Create a second device that is not owned by the user
        # and should not show in the list.
        AuthorizedDeviceFactory.create(
            public_key=generate_rsa_keys()[1].exportKey('DER')
        )

        client = TestClient(keybar_liveserver, device_id=device.id, secret=PRIVATE_KEY)
        response = client.list_devices()

        assert response.status_code == 200
        assert response.json() == [{
            'name': device.name,
            'id': str(device.id),
            'authorized': True
        }]
