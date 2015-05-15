import pytest
import mock

from keybar.client import Client
from keybar.models.device import Device

from keybar.tests.factories.device import (
    AuthorizedDeviceFactory, PUBLIC_KEY, PRIVATE_KEY)
from keybar.tests.factories.user import UserFactory


@pytest.mark.django_db(transaction=True)
class TestDevicesEndpoint:

    def test_register(self, keybar_liveserver):
        client = Client()

        endpoint = '{0}/api/devices/register/'.format(keybar_liveserver.url)

        response = client.post(endpoint, data={
            'name': 'Test Device',
            'public_key': str(PUBLIC_KEY.exportKey('PEM'), 'ascii')
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
        client = Client(device.id, PRIVATE_KEY)

        endpoint = '{0}/api/devices/'.format(keybar_liveserver.url)

        response = client.get(endpoint)

        assert response.status_code == 200
        assert response.json() == [{
            'name': device.name,
            'id': str(device.id),
            'authorized': True
        }]
