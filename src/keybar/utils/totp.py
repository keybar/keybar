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


BASE_URI = 'otpauth://{key_type}/{issuer}:{user}?secret={secret}&issuer={issuer}'


def generate_qr_code_response(request):
    user = request.user

    domain = urllib.parse.urlparse(request.build_absolute_uri()).netloc

    qrcode = QRCode()

    uri = generate_uri('totp', bytes(user.totp_secret), user.email, 'keybar')

    print(uri)

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
    return BASE_URI.format(**{
        'key_type': urllib.parse.quote(key_type),
        'issuer': urllib.parse.quote(issuer),
        'user': urllib.parse.quote(user),
        'secret': urllib.parse.quote(b32encode(secret))
    })


def verify_totp_code(user, code):
    totp = TOTP(bytes(user.totp_secret), 6, SHA1(), 30, backend=default_backend())
    return totp.verify(force_bytes(code), time.time())
