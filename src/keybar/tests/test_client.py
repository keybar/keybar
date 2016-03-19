import os

import pytest
import requests

from keybar.client import TLS12SSLAdapter
from keybar.tests.helpers import LiveServerTest
from keybar.tests.factories.user import UserFactory
from keybar.tests.factories.device import (
    AuthorizedDeviceFactory, PRIVATE_KEY, PRIVATE_KEY2)
from keybar.utils.http import InsecureTransport


def verify_rejected_ssl(url):
    """
    The utility verifies that the url raises SSLError if the remote server
    supports only weak ciphers.
    """
    with pytest.raises(requests.exceptions.SSLError):
        session = requests.Session()
        session.mount('https://', TLS12SSLAdapter())

        session.get(url)
    return True


@pytest.mark.django_db(transaction=True)
class TestTestClient(LiveServerTest):
    def test_url_must_be_https(self):
        client = self.get_client(None, None)

        with pytest.raises(InsecureTransport):
            client.get('http://fails.xy')

    def test_simple_unauthorized(self):
        user = UserFactory.create()
        device = AuthorizedDeviceFactory.create(user=user)

        client = self.get_client(device.id, None)

        endpoint = '{0}/api/dummy/'.format(self.liveserver.url)

        response = client.get(endpoint)

        assert response.status_code == 401

    def test_simple_authorized(self):
        user = UserFactory.create(is_superuser=True)
        device = AuthorizedDeviceFactory.create(user=user)

        client = self.get_client(device.id, PRIVATE_KEY)

        endpoint = '{0}/api/dummy/'.format(self.liveserver.url)

        response = client.get(endpoint)

        assert response.status_code == 200
        assert response.content == b'"{\\"dummy\\":\\"ok\\"}"'

    def test_simple_wrong_device_secret(self, settings):
        user = UserFactory.create(is_superuser=True)
        device = AuthorizedDeviceFactory.create(user=user)

        client = self.get_client(device.id, PRIVATE_KEY2)

        endpoint = '{0}/api/dummy/'.format(self.liveserver.url)

        response = client.get(endpoint)
        assert response.status_code == 401
        assert response.json()['detail'] == 'Error decoding signature.'

    def test_to_server_without_tls_10(self, allow_offline):
        """
        Verify that connection is possible to SFDC servers that disabled TLS 1.0
        """
        session = requests.Session()
        session.mount('https://', TLS12SSLAdapter())

        response = session.get('https://tls1test.salesforce.com/s/')
        assert response.status_code == 200

    def test_under_downgrade_attack_to_ssl_3(self, allow_offline):
        """
        Verify that the connection is rejected if the remote server (or man
        in the middle) claims that SSLv3 is the best supported protocol.
        """
        url = 'https://ssl3.zmap.io/sslv3test.js'
        assert verify_rejected_ssl(url)

    def test_protocols_by_ssl_labs(self, allow_offline):
        session = requests.Session()
        session.mount('https://', TLS12SSLAdapter())
        response = session.get('https://www.ssllabs.com/ssltest/viewMyClient.html')

        assert 'Your user agent has good protocol support' in response.text

    @pytest.mark.skipif(os.environ.get('ON_TRAVIS', None) == 'true', reason='on travis')
    def test_sni_suport(self, allow_offline):
        session = requests.Session()
        session.mount('https://', TLS12SSLAdapter())
        response = session.get('https://sni.velox.ch/')
        assert 'sent the following TLS server name indication extension' in response.text
        assert 'negotiated protocol: TLSv1.2' in response.text

    @pytest.mark.skipif(os.environ.get('ON_TRAVIS', None) == 'true', reason='on travis')
    def test_vulnerability_logjam_by_ssl_labs(self, allow_offline):
        assert verify_rejected_ssl('https://www.ssllabs.com:10445/')

    def test_vulnerability_freak_by_ssl_labs(self, allow_offline):
        assert verify_rejected_ssl('https://www.ssllabs.com:10444/')

    def test_vulnerability_osx_by_ssl_labs(self, allow_offline):
        assert verify_rejected_ssl('https://www.ssllabs.com:10443/')
