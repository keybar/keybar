import os

import pytest

from keybar.client import Client
from keybar.utils.http import InsecureTransport

from keybar.tests.factories.user import UserFactory
from keybar.tests.factories.device import DeviceFactory


@pytest.mark.django_db(transaction=True)
class TestClient(object):

    def test_url_must_be_https(self):
        client = Client(None, None)

        with pytest.raises(InsecureTransport):
            client.get('http://fails.xy')

    def test_simple(self, settings, keybar_liveserver):
        settings.DEBUG = True

        fpath = os.path.join(settings.PROJECT_DIR, 'extras', 'example_keys', 'id_rsa')

        with open(fpath, 'rb') as fobj:
            secret = fobj.read()

        user = UserFactory.create(is_superuser=True)
        device = DeviceFactory.create(user=user)

        client = Client(device.id.hex, secret)

        endpoint = '{0}/api/v1/users/'.format(keybar_liveserver.url)

        response = client.get(endpoint)

        assert response.status_code == 200
