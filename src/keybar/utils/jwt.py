from datetime import datetime, timedelta

import jwt
from django.conf import settings

from keybar.utils.crypto import load_private_key


JWT_OPTIONS = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': True,
    'verify_iat': True,
    'verify_aud': True,
    'require_exp': True,
    'require_iat': True,
    'require_nbf': True
}

LEEWAY = 10
EXPIRATION_DELTA = timedelta(seconds=60)


def decode_token(token, device):
    return jwt.decode(
        token,
        verify=True,
        key=device.loaded_public_key,
        options=JWT_OPTIONS,
        leeway=LEEWAY,
        audience=settings.KEYBAR_HOST,
        algorithms=['RS256']
    )


def encode_token(device_id, private_key):
    # TODO: make aud configurable
    issued_at = datetime.utcnow()
    payload = {
        'iss': device_id,
        'exp': issued_at + EXPIRATION_DELTA,
        'iat': issued_at,
        'nbf': issued_at,
        'aud': 'local.keybar.io:9999',
    }

    return jwt.encode(
        payload,
        key=load_private_key(private_key),
        algorithm='RS256'
    ).decode('utf-8')
