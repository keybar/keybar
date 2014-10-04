import hashlib
import ssl
import os
from itertools import cycle

from django.conf import settings
from cryptography.fernet import Fernet

# Verify we can use all feature we require.
assert ssl.HAS_ECDH
assert ssl.HAS_SNI


def xor_strings(string, key):
    assert isinstance(string, (bytes, bytearray))
    assert isinstance(key, (bytes, bytearray))

    base = bytearray(string)

    return bytearray(char ^ k for char, k in zip(base, cycle(key)))


def pbkdf2(salt, password):
    iterations = settings.KEYBAR_KDF_ITERATIONS
    return hashlib.pbkdf2_hmac('sha256', salt, password, iterations)


def derive_encryption_key_spec(password):
    """Get the real encryption key.

    Don't use the password directly but derive a encryption key
    dynamically based on the password and a stored key.

    This allows for password and encryption key to be changed
    independently, e.g in case of a security breach.

    :return: A string of ``16-byte-salt$key``.
    """
    fernet_key = Fernet.generate_key()
    salt = os.urandom(16)
    hashed_value = pbkdf2(salt, password)

    # Ordering of the xor-arguments is important, because of
    # very simplified xor-implementation.
    visible_key = xor_strings(fernet_key, hashed_value)

    return salt + b'$' + visible_key


def get_encryption_key(key, password):
    # We must split only once. The Fernet key can also contain
    # `$` characters
    salt, visible_key = bytes(key).split(b'$', 1)
    hashed_value = pbkdf2(salt, password)

    # Ordering of the xor-arguments is important, because of
    # very simplified xor-implementation.
    return xor_strings(visible_key, hashed_value)


def get_server_context(verify=True):
    """Our TLS configuration for the server"""
    server_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

    server_ctx.set_ecdh_curve('prime256v1')
    server_ctx.verify_mode = ssl.CERT_OPTIONAL if not verify else ssl.CERT_REQUIRED

    # ECDHE appears to be preferred to RSA in many ways,
    # unfortunately it does not seem to work (getting handshake failures)
    # server_ctx.set_ciphers('ECDH-ECDSA-AES256-GCM-SHA384')

    # (cg) unfortunately somehow on my dev machine chromium does not support
    # aes256 + sha384 so I'm degrading for now to allow for
    # Web UI development without hassles :-/

    # server_ctx.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384')
    server_ctx.set_ciphers('ECDHE-RSA-AES128-GCM-SHA256')

    # Mitigate CRIME
    server_ctx.options |= ssl.OP_NO_COMPRESSION

    # Prevents re-use of the same ECDH key for distinct SSL sessions.
    # This improves forward secrecy but requires more computational resources.
    server_ctx.options |= ssl.OP_SINGLE_ECDH_USE

    # Use the server’s cipher ordering preference, rather than the client’s.
    server_ctx.options |= ssl.OP_CIPHER_SERVER_PREFERENCE

    # Load the certificates
    server_ctx.load_cert_chain(
        settings.KEYBAR_SERVER_CERTIFICATE,
        settings.KEYBAR_SERVER_KEY
    )

    server_ctx.load_verify_locations(settings.KEYBAR_CA_BUNDLE)

    return server_ctx


def get_client_context(verify=True):
    """Matching TLS configuration for the client."""
    client_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

    client_ctx.verify_mode = ssl.CERT_OPTIONAL if not verify else ssl.CERT_REQUIRED

    # Require checking the hostname
    client_ctx.check_hostname = True

    # Same as the server.
    # server_ctx.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384')
    client_ctx.set_ciphers('ECDHE-RSA-AES128-GCM-SHA256')

    # Mitigate CRIME
    client_ctx.options |= ssl.OP_NO_COMPRESSION

    # Load the certificates
    client_ctx.load_cert_chain(
        settings.KEYBAR_CLIENT_CERTIFICATE,
        settings.KEYBAR_CLIENT_KEY
    )

    client_ctx.load_verify_locations(settings.KEYBAR_CA_BUNDLE)

    return client_ctx


def _patch_ssl_for_tlsv12_default():
    import ssl
    from functools import wraps

    def sslwrap(func):
        @wraps(func)
        def wrapper(*args, **kw):
            kw['ssl_version'] = ssl.PROTOCOL_TLSv1_2
            return func(*args, **kw)
        return wrapper

    ssl.wrap_socket = sslwrap(ssl.wrap_socket)
