import pytest
import mock

from keybar.client import Client

from keybar.tests.factories.device import PUBLIC_KEY


@pytest.mark.django_db(transaction=True)
class TestDevicesEndpoint:

    @pytest.fixture(autouse=True)
    def setup(self, settings, keybar_liveserver):
        self.liveserver = keybar_liveserver

    def test_register(self):
        client = Client()

        endpoint = '{0}/api/devices/register/'.format(self.liveserver.url)

        response = client.post(endpoint, data={
            'name': 'Test Device',
            'public_key': str(PUBLIC_KEY.exportKey('PEM'), 'ascii')
        })

        assert response.status_code == 200
        assert response.json() == {
            'name': 'Test Device',
            'id': mock.ANY,
        }
