from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from httpsig import Verifier
from httpsig.utils import HttpSigException, parse_authorization_header, generate_message

from keybar.models.device import Device


ALGORITHM = 'rsa-sha256'
REQUIRED_HEADERS = ['(request-target)', 'accept', 'date', 'host']


def normalize(value):
    if value.startswith('HTTP_') or value in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
        return value[5:].lower().replace('_', '-')
    return value.lower().replace('_', '-')


class PrefixStripingCaseInsensitiveDict(dict):
    """Customized to support striping HTTP_ prefixes"""
    def __init__(self, meta=None, **kwargs):
        super(PrefixStripingCaseInsensitiveDict, self).__init__(**kwargs)
        if meta:
            self.update((normalize(key), value) for key, value in meta.items())

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
            self.auth_method, self.auth_fields = auth

            # Ignore foreign Authorization headers
            if self.auth_method.lower() != 'signature':
                raise HttpSigException('Invalid authorization header.')
        else:
            raise HttpSigException('Invalid authorization header.')

        self.headers = PrefixStripingCaseInsensitiveDict(request.META)
        self.required_headers = [key.lower() for key in required_headers]
        self.method = method
        self.path = path
        self.host = host

        super(HeaderVerifier, self).__init__(secret, algorithm=self.auth_fields['algorithm'])

    def verify(self):
        auth_headers = self.auth_fields.get('headers', 'date').split(' ')

        if len(set(self.required_headers) - set(auth_headers)) > 0:
            required_headers = ', '.join(set(self.required_headers) - set(auth_headers))
            msg = '{} is a required header(s)'.format(required_headers)
            raise HttpSigException(msg)

        signing_str = generate_message(
            auth_headers, self.headers, self.host, self.method, self.path)

        return self._verify(signing_str, self.auth_fields['signature'])


class KeybarApiSignatureAuthentication(BaseAuthentication):
    """Our own implementation of HTTP Signature authentication.

    We need to implement this our own as no existing library uses `httpsig`
    package correctly and actually verfies the signature in a correct manner
    (e.g using HeaderVerifier)
    """
    www_authenticate_realm = 'keybar-api'

    def get_host(self, request):
        return settings.KEYBAR_HOST

    def get_device(self, request):
        device_id = request.META.get('HTTP_X_DEVICE_ID')
        device = Device.objects.get(pk=device_id)
        return device

    def authenticate(self, request):
        try:
            device = self.get_device(request)
        except (TypeError, Device.DoesNotExist):
            raise exceptions.AuthenticationFailed('Bad device id')

        try:
            verifier = HeaderVerifier(
                request=request,
                secret=device.public_key,
                required_headers=REQUIRED_HEADERS,
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

        return (device.user, None)

    def authenticate_header(self, request):
        headers = ' '.join(REQUIRED_HEADERS)
        return 'Signature realm="{realm}",headers="{headers}"'.format(
            realm=self.www_authenticate_realm, headers=headers,
        )
