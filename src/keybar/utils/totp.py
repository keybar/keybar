import io
import urllib
import time
from base64 import b32encode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from cryptography.hazmat.primitives.hashes import SHA1
from django.http import HttpResponse
from django.utils.encoding import force_bytes
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_H


BASE_URI = 'otpauth://{key_type}/{issuer}:{user}?secret={secret}&issuer={issuer}'


def generate_qr_code_response(request):
    user = request.user

    qrcode = QRCode(
        error_correction=ERROR_CORRECT_H,
        box_size=4,
        border=4
    )

    uri = generate_uri('totp', bytes(user.secret), user.email, 'keybar')

    qrcode.add_data(uri)
    qrcode.make(fit=True)
    img = qrcode.make_image()

    stream = io.BytesIO()
    img.save(stream)

    return HttpResponse(stream.getvalue(), content_type='image/png')


def generate_uri(key_type, secret, user, issuer):
    """Generate a URI suitable for Google Authenticator.

    See: https://code.google.com/p/google-authenticator/wiki/KeyUriFormat
    """
    # Google Authenticator breaks if the b32 encoded string contains a padding
    # thus force the key to be divisible by 5 octets so that we don't have any
    # padding markers.
    assert len(secret) % 5 == 0, 'secret not divisible by 5'

    return BASE_URI.format(**{
        'key_type': urllib.parse.quote(key_type),
        'issuer': urllib.parse.quote(issuer),
        'user': urllib.parse.quote(user),
        'secret': urllib.parse.quote(b32encode(secret)),
    })


def verify_totp_code(user, code):
    totp = TOTP(bytes(user.secret), 6, SHA1(), 30, backend=default_backend())
    return totp.verify(force_bytes(code), time.time())
