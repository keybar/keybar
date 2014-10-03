import os

from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from httpsig import Verifier
from httpsig.utils import HttpSigException, parse_authorization_header, generate_message

from keybar.models.device import Device


def normalize(value):
    if value.startswith('HTTP_'):
        return value[5:].lower().replace('_', '-')
    return value.lower().replace('_', '-')


class PrefixStripingCaseInsensitiveDict(dict):
    """Customized to support striping HTTP_ prefixes"""
    def __init__(self, d=None, **kwargs):
        super(PrefixStripingCaseInsensitiveDict, self).__init__(**kwargs)
        if d:
            self.update((normalize(k), v) for k, v in d.items())

    def __setitem__(self, key, value):
        super(PrefixStripingCaseInsensitiveDict, self).__setitem__(normalize(key), value)

    def __getitem__(self, key):
        return super(PrefixStripingCaseInsensitiveDict, self).__getitem__(normalize(key))

    def __contains__(self, key):
        return super(PrefixStripingCaseInsensitiveDict, self).__contains__(normalize(key))


class HeaderVerifier(Verifier):
    """Custom header verifier to support django specific header-names..."""

    def __init__(self, request, secret, required_headers=None, method=None,
                 path=None, host=None):
        self.request = request
        required_headers = required_headers or ['date']

        auth = parse_authorization_header(get_authorization_header(request))

        if len(auth) == 2:
            self.auth_dict = auth[1]
        else:
            raise HttpSigException("Invalid authorization header.")

        self.headers = PrefixStripingCaseInsensitiveDict(request.META)
        self.required_headers = [key.lower() for key in required_headers]
        self.method = method
        self.path = path
        self.host = host

        super(HeaderVerifier, self).__init__(secret, algorithm=self.auth_dict['algorithm'])

    def verify(self):
        auth_headers = self.auth_dict.get('headers', 'date').split(' ')

        if len(set(self.required_headers) - set(auth_headers)) > 0:
            required_headers = ', '.join(set(self.required_headers) - set(auth_headers))
            msg = '{} is a required header(s)'.format(required_headers)
            raise HttpSigException(msg)

        signing_str = generate_message(
            auth_headers, self.headers, self.host, self.method, self.path)

        return self._verify(signing_str, self.auth_dict['signature'])


class KeybarApiSignatureAuthentication(BaseAuthentication):
    """Our own implementation of HTTP Signature authentication.

    We need to implement this our own as no existing library uses `httpsig`
    package correctly and actually verfies the signature in a correct manner
    (e.g using HeaderVerifier)
    """

    API_KEY_HEADER = 'X-Api-Key'
    ALGORITHM = 'rsa-sha256'
    REQUIRED_HEADERS = ['(request-target)', 'accept', 'date', 'host']

    def get_verify_secret(self, request):
        # TODO: Fetch that public key from the device
        fpath = os.path.join(
            settings.PROJECT_DIR, 'extras', 'example_keys', 'id_rsa.pub')

        with open(fpath, 'rb') as fobj:
            secret = fobj.read()

        return secret

    def get_host(self, request):
        return settings.KEYBAR_HOST

    def fetch_user(self, request):
        # TODO: fetch device_id from the device…
        device_id = request.META.get('HTTP_X_DEVICE_ID')
        device = Device.objects.get(pk=device_id)
        return device.user

    def authenticate(self, request):
        try:
            verifier = HeaderVerifier(
                request=request,
                secret=self.get_verify_secret(request),
                required_headers=self.REQUIRED_HEADERS,
                host=self.get_host(request),
                method=request.method,
                path=request.path)
        except HttpSigException as exc:
            raise exceptions.AuthenticationFailed(exc.message)

        try:
            if not verifier.verify():
                raise exceptions.AuthenticationFailed('Bad signature')
        except HttpSigException as exc:
            raise exceptions.AuthenticationFailed(exc.message)

        try:
            user = self.fetch_user(request)
        except TypeError:
            raise exceptions.AuthenticationFailed('Bad device id')

        return (user, None)

    def authenticate_header(self, request):
        # TODO:
        return super(KeybarApiSignatureAuthentication, self).authenticate_header(request)
