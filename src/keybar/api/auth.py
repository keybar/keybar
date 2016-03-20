import jwt

from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header
)

from keybar.models.device import Device
from keybar.utils.jwt import decode_token


class JSONWebTokenAuthentication(BaseAuthentication):
    """Token based authentication using the JSON Web Token standard.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "JWT".

    .. code-block::

        Authorization: JWT eyJhbGciOiAiSFMyNTYiLCAidHlwIj...
    """
    www_authenticate_realm = 'api'
    auth_header_prefix = 'JWT'

    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = self.auth_header_prefix.lower()

        if not auth or smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate(self, request):
        """Authenticate `request`.

        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(request)

        if jwt_value is None:
            return None

        unverified_data = jwt.decode(jwt_value, verify=False)

        if 'iss' not in unverified_data:
            msg = 'JWT iss (issuer) claim is missing'
            raise exceptions.AuthenticationFailed(detail=msg)

        device = Device.objects.get(pk=unverified_data['iss'])

        try:
            payload = decode_token(jwt_value, device)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        if unverified_data['iss'] != payload['iss']:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(device)

        return (user, jwt_value)

    def authenticate_credentials(self, device):
        # TODO:
        # if not user.is_active:
        #     msg = _('User account is disabled.')
        #     raise exceptions.AuthenticationFailed(msg)

        return device.user

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format(self.auth_header_prefix, self.www_authenticate_realm)
