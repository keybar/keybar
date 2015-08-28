import hashlib
import ssl
import urllib
import uuid
from base64 import encodebytes
from datetime import datetime
from email.utils import formatdate
from time import mktime

import pkg_resources
import requests
from django.conf import settings
from django.utils.encoding import force_bytes
from httpsig.requests_auth import HTTPSignatureAuth
from requests_toolbelt import SSLAdapter, user_agent

from keybar.api.auth import ALGORITHM, REQUIRED_HEADERS
from keybar.utils import json
from keybar.utils.http import InsecureTransport, is_secure_transport


class TLS12SSLAdapter(SSLAdapter):

    def __init__(self, *args, **kwargs):
        self.ssl_version = ssl.PROTOCOL_TLSv1_2
        super(TLS12SSLAdapter, self).__init__(**kwargs)


class Client(requests.Session):
    """Proof of concept client implementation."""
    content_type = 'application/json'

    def __init__(self, device_id=None, secret=None):
        super(Client, self).__init__()

        self.mount('https://', TLS12SSLAdapter())

        if isinstance(device_id, uuid.UUID):
            self.device_id = device_id.hex
        else:
            self.device_id = device_id

        if secret and not isinstance(secret, (bytes, str)):
            secret = secret.exportKey('PEM')

        self.secret = secret

        # Force enabling certificate checking for this session.
        self.verify = settings.KEYBAR_CA_BUNDLE

    def request(self, method, url, *args, **kwargs):
        if not is_secure_transport(url):
            raise InsecureTransport('Please make sure to use HTTPS')

        data = kwargs.get('data', {})

        now = datetime.utcnow()
        stamp = mktime(now.timetuple())

        raw_data = force_bytes(json.dumps(data))
        content_md5 = encodebytes(hashlib.md5(raw_data).digest()).strip()

        parse_result = urllib.parse.urlparse(url)

        dist = pkg_resources.get_distribution('keybar')

        headers = {
            'User-Agent': user_agent('keybar', dist.version),
            'Host': parse_result.netloc,
            'Method': method,
            'Path': parse_result.path,
            'Accept': self.content_type,
            'X-Device-Id': self.device_id,
            'Content-MD5': content_md5,
            'Date': formatdate(timeval=stamp, localtime=False, usegmt=True)
        }

        headers.update(kwargs.pop('headers', {}))

        if self.device_id and self.secret:
            auth = HTTPSignatureAuth(
                key_id=self.device_id,
                secret=self.secret,
                headers=REQUIRED_HEADERS,
                algorithm=ALGORITHM)
        else:
            auth = ()

        kwargs.update({
            'auth': auth,
            'headers': headers,
            'data': data,
            'cert': (settings.KEYBAR_CLIENT_CERTIFICATE, settings.KEYBAR_CLIENT_KEY),
            'verify': settings.KEYBAR_CA_BUNDLE,
        })

        return super(Client, self).request(method, url, *args, **kwargs)
