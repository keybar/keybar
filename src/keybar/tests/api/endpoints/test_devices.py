import mock
import pytest

from keybar.client import Client
from keybar.models.device import Device
from keybar.tests.factories.device import PRIVATE_KEY, PUBLIC_KEY, AuthorizedDeviceFactory
from keybar.tests.factories.user import UserFactory
from keybar.utils.crypto import generate_rsa_keys, serialize_public_key


@pytest.mark.django_db(transaction=True)
class TestDevicesEndpoint:

    def test_register(self, keybar_liveserver):
        client = Client()

        endpoint = '{0}/api/devices/register/'.format(keybar_liveserver.url)

        response = client.post(endpoint, data={
            'name': 'Test Device',
            'public_key': serialize_public_key(PUBLIC_KEY)
        })

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
            public_key=serialize_public_key(generate_rsa_keys()[1])
        )

        client = Client(device.id, PRIVATE_KEY)

        endpoint = '{0}/api/devices/'.format(keybar_liveserver.url)

        response = client.get(endpoint)

        assert response.status_code == 200
        assert response.json() == [{
            'name': device.name,
            'id': str(device.id),
            'authorized': True
        }]
