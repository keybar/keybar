import hashlib
import json
from base64 import encodebytes
from datetime import datetime
from email.utils import formatdate
from time import mktime

import pytest
import requests
from django.utils.encoding import force_bytes
from httpsig.requests_auth import HTTPSignatureAuth
from rest_framework import status

from keybar.client import TLS12SSLAdapter
from keybar.tests.factories.device import PRIVATE_KEY, AuthorizedDeviceFactory
from keybar.tests.factories.user import UserFactory
from keybar.utils.crypto import serialize_private_key


@pytest.mark.django_db(transaction=True)
class TestHttpSignatureAuth:

    def test_simple_success(self, settings, keybar_liveserver):
        user = UserFactory.create(is_superuser=True)
        device = AuthorizedDeviceFactory.create(user=user)

        signature_headers = ['(request-target)', 'accept', 'date', 'host']

        now = datetime.now()
        stamp = mktime(now.timetuple())

        data = {}
        content_md5 = encodebytes(hashlib.md5(
            force_bytes(json.dumps(data))).digest()).strip()

        headers = {
            'Host': keybar_liveserver.domain,
            'Method': 'GET',
            'Path': '/api/users/',
            'Accept': 'application/json',
            'X-Device-Id': device.id.hex,
            'Content-MD5': content_md5,
            'Date': formatdate(timeval=stamp, localtime=False, usegmt=True)
        }

        auth = HTTPSignatureAuth(
            key_id=device.id.hex,
            secret=serialize_private_key(PRIVATE_KEY),
            headers=signature_headers,
            algorithm='rsa-sha256')

        session = requests.Session()
        session.mount(keybar_liveserver.url, TLS12SSLAdapter())

        response = session.get(
            '{0}/api/users/'.format(keybar_liveserver.url),
            auth=auth,
            headers=headers,
            cert=(settings.KEYBAR_CLIENT_CERTIFICATE, settings.KEYBAR_CLIENT_KEY),
            verify=settings.KEYBAR_CA_BUNDLE)

        assert response.status_code == status.HTTP_200_OK

    def test_simple_fail(self, settings, keybar_liveserver):
        session = requests.Session()
        session.mount(keybar_liveserver.url, TLS12SSLAdapter())

        response = session.get(
            '{0}/api/users/'.format(keybar_liveserver.url),
            cert=(settings.KEYBAR_CLIENT_CERTIFICATE, settings.KEYBAR_CLIENT_KEY),
            verify=settings.KEYBAR_CA_BUNDLE)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        expected = 'Signature realm="keybar-api",headers="(request-target) accept date host"'
        assert response.headers['WWW-Authenticate'] == expected
