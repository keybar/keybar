import hashlib
import os
import ssl
import json
from email.utils import formatdate
from datetime import datetime
from time import mktime
from base64 import encodebytes

import pytest
import requests
from requests_toolbelt import SSLAdapter
from django.utils.encoding import force_bytes
from rest_framework import status
from httpsig.requests_auth import HTTPSignatureAuth

from keybar.tests.factories.user import UserFactory
from keybar.tests.factories.device import DeviceFactory


@pytest.mark.django_db(transaction=True)
class TestHttpSignatureAuth(object):

    def test_simple_success(self, settings, keybar_liveserver):
        settings.DEBUG = True

        fpath = os.path.join(settings.BASE_DIR, 'tests', 'resources', 'rsa_keys', 'id_rsa')

        with open(fpath, 'rb') as fobj:
            secret = fobj.read()

        user = UserFactory.create(is_superuser=True)
        device = DeviceFactory.create(user=user)

        signature_headers = ['(request-target)', 'accept', 'date', 'host']

        now = datetime.now()
        stamp = mktime(now.timetuple())

        data = {}
        content_md5 = encodebytes(hashlib.md5(
            force_bytes(json.dumps(data))).digest()).strip()

        headers = {
            'Host': keybar_liveserver.domain,
            'Method': 'GET',
            'Path': '/api/v1/users/',
            'Accept': 'application/json',
            'X-Device-Id': device.id.hex,
            'Content-MD5': content_md5,
            'Date': formatdate(timeval=stamp, localtime=False, usegmt=True)
        }

        auth = HTTPSignatureAuth(
            key_id=device.id.hex,
            secret=secret,
            headers=signature_headers,
            algorithm='rsa-sha256')

        session = requests.Session()
        session.mount(keybar_liveserver.url, SSLAdapter(ssl.PROTOCOL_TLSv1_2))

        response = session.get(
            '{0}/api/v1/users/'.format(keybar_liveserver.url),
            auth=auth,
            headers=headers,
            cert=(settings.KEYBAR_CLIENT_CERTIFICATE, settings.KEYBAR_CLIENT_KEY),
            verify=settings.KEYBAR_CA_BUNDLE)

        assert response.status_code == status.HTTP_200_OK

    def test_simple_fail(self, settings, keybar_liveserver):
        settings.DEBUG = True

        session = requests.Session()
        session.mount(keybar_liveserver.url, SSLAdapter(ssl.PROTOCOL_TLSv1_2))

        response = session.get(
            '{0}/api/v1/users/'.format(keybar_liveserver.url),
            cert=(settings.KEYBAR_CLIENT_CERTIFICATE, settings.KEYBAR_CLIENT_KEY),
            verify=settings.KEYBAR_CA_BUNDLE)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        expected = 'Signature realm="keybar-api",headers="(request-target) accept date host"'
        assert response.headers['WWW-Authenticate'] == expected
