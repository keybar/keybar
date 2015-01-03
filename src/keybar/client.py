import hashlib
import ssl
import urllib
import pkg_resources
from email.utils import formatdate
from datetime import datetime
from time import mktime
from base64 import encodebytes

import requests
from requests_toolbelt import SSLAdapter
from requests_toolbelt.user_agent import user_agent
from django.conf import settings
from django.utils.encoding import force_bytes
from httpsig.requests_auth import HTTPSignatureAuth

from keybar.api.auth import ALGORITHM, REQUIRED_HEADERS
from keybar.utils.http import is_secure_transport, InsecureTransport
from keybar.utils import json


class Client(requests.Session):
    content_type = 'application/json'

    def __init__(self, device_id, secret):
        super(Client, self).__init__()

        keybar_url = 'https://{0}'.format(settings.KEYBAR_HOST)
        self.mount(keybar_url, SSLAdapter(ssl.PROTOCOL_TLSv1_2))
        self.device_id = device_id

        # TODO: find a way to avoid holding this in-memory for too long.
        self.secret = secret

    def request(self, method, url, *args, **kwargs):
        if not is_secure_transport(url):
            raise InsecureTransport('Please make sure to use HTTPS')

        data = kwargs.pop('data', {})

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

        auth = HTTPSignatureAuth(
            key_id=self.device_id,
            secret=self.secret,
            headers=REQUIRED_HEADERS,
            algorithm=ALGORITHM)

        kwargs.update({
            'auth': auth,
            'headers': headers,
            'cert': (settings.KEYBAR_CLIENT_CERTIFICATE, settings.KEYBAR_CLIENT_KEY),
            'verify': settings.KEYBAR_CA_BUNDLE,
        })

        return super(Client, self).request(method, url, *args, **kwargs)
