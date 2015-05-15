import pytest
import mock

from keybar.client import Client
from keybar.models.device import Device

from keybar.tests.factories.device import PUBLIC_KEY


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
        }

        assert Device.objects.get().user is None
