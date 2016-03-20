import ssl
import urllib
import uuid
from urllib.parse import urlencode, urljoin

import pkg_resources
import requests
from django.conf import settings
from requests_toolbelt import SSLAdapter, user_agent

from keybar.utils.http import InsecureTransport, InvalidHost, is_secure_transport, verify_host
from keybar.utils.crypto import serialize_private_key
from keybar.utils.jwt import encode_token


class TLS12SSLAdapter(SSLAdapter):

    def __init__(self, *args, **kwargs):
        kwargs['ssl_version'] = ssl.PROTOCOL_TLSv1_2
        super(TLS12SSLAdapter, self).__init__(**kwargs)


class APIError(Exception):
    def __init__(self, message, code=0):
        self.code = code
        self.message = message

    def __str__(self):
        return '{}: {}'.format(self.message, self.code)


class Client(requests.Session):
    """Proof of concept client implementation."""
    content_type = 'application/vnd.keybar+json'

    host = 'keybar.me'
    port = '443'
    timeout = 3.0

    def __init__(self, device_id=None, secret=None):
        super(Client, self).__init__()

        self.mount('https://', TLS12SSLAdapter())

        if isinstance(device_id, uuid.UUID):
            self.device_id = device_id.hex
        else:
            self.device_id = device_id

        if secret and not isinstance(secret, (bytes, str)):
            secret = serialize_private_key(secret)

        self.secret = secret

        # Force enabling certificate checking for this session.
        self.verify = settings.KEYBAR_CA_BUNDLE

    def build_url(self, endpoint, qs=None):
        url = urljoin(
            'https://{host}:{port}'.format(host=self.host, port=self.port),
            endpoint)

        if qs:
            url += '?' + urlencode(qs)
        return url

    def request(self, method, url, *args, **kwargs):
        if not is_secure_transport(url):
            raise InsecureTransport('Please make sure to use HTTPS')

        if not verify_host(url, [self.host]):
            raise InvalidHost(
                'Please verify the client is using "{}" has host'.format(self.host))

        data = kwargs.get('data', {})

        parse_result = urllib.parse.urlparse(url)

        dist = pkg_resources.get_distribution('keybar')

        headers = {
            'User-Agent': user_agent('keybar', dist.version),
            'Host': parse_result.netloc,
            'Method': method,
            'Path': parse_result.path,
            'Accept': self.content_type,
            'Content-Type': self.content_type,
        }

        if self.device_id and self.secret:
            headers['Authorization'] = 'JWT {}'.format(
                encode_token(self.device_id, self.secret)
            )

        headers.update(kwargs.pop('headers', {}))

        kwargs.update({
            'headers': headers,
            'data': data,
            'cert': (settings.KEYBAR_CLIENT_CERTIFICATE, settings.KEYBAR_CLIENT_KEY),
            'verify': settings.KEYBAR_CA_BUNDLE,
            'timeout': self.timeout
        })

        return super(Client, self).request(method, url, *args, **kwargs)

    def _api_request(self, method, *args, **kwargs):
        try:
            response = self.request(method, *args, **kwargs)
        except requests.HTTPError as exc:
            # TODO: Get this from API header or so...
            msg = 'lalalal'
            code = exc.getcode()

            if msg:
                raise APIError(msg, code)
            else:
                raise exc

        return response


class LocalClient(Client):
    host = 'local.keybar.io'
    port = '8443'
