import os
import ssl
from email.utils import formatdate
from datetime import datetime
from time import mktime

import pytest
import requests
from requests_toolbelt import SSLAdapter
from django.conf import settings
from django.utils import timezone
from httpsig.requests_auth import HTTPSignatureAuth

from keybar.models.user import User
from keybar.tests.factories.user import UserFactory


@pytest.mark.django_db(transaction=True)
class TestHttpSignatureAuth(object):

    def test_simple(self, settings, keybar_liveserver):
        settings.DEBUG = True

        fpath = os.path.join(
                settings.PROJECT_DIR, 'extras', 'example_keys', 'private_key.pem')

        with open(fpath, 'rb') as fobj:
            secret = fobj.read()

        user = UserFactory.create(is_superuser=True)

        signature_headers = ['(request-target)', 'accept', 'date', 'host']

        now = datetime.now()
        stamp = mktime(now.timetuple())

        headers = {
            'Host': keybar_liveserver.domain,
            'Method': 'GET',
            'Path': '/api/v1/users/',
            'Accept': 'application/json',
            'X-Api-Key': user.api_key.hex,
            'Date': formatdate(timeval=stamp, localtime=False, usegmt=True)
        }

        auth = HTTPSignatureAuth(
            key_id=user.api_key.hex,
            secret=secret,
            headers=signature_headers,
            algorithm='rsa-sha256')

        session = requests.Session()
        session.mount(keybar_liveserver.url, SSLAdapter(ssl.PROTOCOL_TLSv1_2))

        response = session.get(
            '{0}/api/v1/users/'.format(keybar_liveserver.url),
            auth=auth,
            headers=headers,
            verify=settings.KEYBAR_CA_BUNDLE)

        assert response.status_code == 200
