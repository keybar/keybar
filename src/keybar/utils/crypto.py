import base64
import ssl
import os

from django.conf import settings
from django.utils.encoding import force_bytes, force_text
from cryptography.fernet import Fernet

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


# Verify we can use all feature we require.
assert ssl.HAS_ECDH
assert ssl.HAS_SNI


def derive_encryption_key_spec(password):
    """Get the real encryption key.

    Don't use the password directly but derive a encryption key
    dynamically based on the password and a stored key.

    This allows for password and encryption key to be changed
    independently, e.g in case of a security breach.

    :return: A string of ``16-byte-salt$key``.
    """
    salt = os.urandom(16)
    backend = default_backend()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=settings.KEYBAR_KDF_ITERATIONS,
        backend=backend
    )

    key = kdf.derive(force_bytes(password))

    encoded_key = base64.urlsafe_b64encode(key)

    return salt + b'$' + encoded_key


def get_encryption_key(key, password):
    # We must split only once. The Fernet key can also contain
    # `$` characters
    salt, encoded_key = bytes(key).split(b'$', 1)
    decoded_key = base64.urlsafe_b64decode(encoded_key)

    backend = default_backend()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=settings.KEYBAR_KDF_ITERATIONS,
        backend=backend
    )

    kdf.verify(force_bytes(password), decoded_key)

    return decoded_key


def encrypt(text, encryption_key):
    fernet = Fernet(base64.urlsafe_b64encode(encryption_key))
    return fernet.encrypt(force_bytes(text))


def decrypt(encrypted_text, encryption_key):
    fernet = Fernet(base64.urlsafe_b64encode(encryption_key))
    return force_text(fernet.decrypt(force_bytes(encrypted_text)))


def get_server_context(verify=True):
    """Our TLS configuration for the server"""
    server_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

    server_ctx.set_ecdh_curve('prime256v1')
    server_ctx.verify_mode = ssl.CERT_OPTIONAL if not verify else ssl.CERT_REQUIRED

    # This list is based on the official supported ciphers by CloudFlare
    # (cloudflare/sslconfig on GitHub) but is again just a tiny little bit
    # more restricted as we force best security available.
    server_ctx.set_ciphers('EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256')

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
    client_ctx.set_ciphers('EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256')

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
