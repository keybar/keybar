import os

import pytest

from keybar.client import Client
from keybar.utils.http import InsecureTransport

from keybar.tests.factories.user import UserFactory
from keybar.tests.factories.device import DeviceFactory, PRIVATE_KEY


@pytest.mark.django_db(transaction=True)
class TestClient(object):

    def test_url_must_be_https(self):
        client = Client(None, None)

        with pytest.raises(InsecureTransport):
            client.get('http://fails.xy')

    def test_simple(self, settings, keybar_liveserver):
        settings.DEBUG = True

        user = UserFactory.create(is_superuser=True)
        device = DeviceFactory.create(user=user)

        client = Client(device.id.hex, PRIVATE_KEY)

        endpoint = '{0}/api/v1/users/'.format(keybar_liveserver.url)

        response = client.get(endpoint)

        assert response.status_code == 200

    def test_simple_wrong_device_secret(self, settings, keybar_liveserver):
        settings.DEBUG = True

        user = UserFactory.create(is_superuser=True)
        device = DeviceFactory.create(user=user)

        fpath = os.path.join(settings.PROJECT_DIR, 'extras', 'example_keys', 'id_rsa2')

        with open(fpath, 'rb') as fobj:
            wrong_secret = fobj.read()

        client = Client(device.id.hex, wrong_secret)

        endpoint = '{0}/api/v1/users/'.format(keybar_liveserver.url)

        response = client.get(endpoint)
        assert response.status_code == 401
        assert response.json()['detail'] == 'Bad signature'
