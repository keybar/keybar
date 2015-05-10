import os
import base64
import ssl

from django.conf import settings
from django.utils.encoding import force_bytes
from cryptography.fernet import Fernet

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


# Verify we can use all feature we require.
assert ssl.HAS_ECDH
assert ssl.HAS_SNI


KEY_LENGTH = 32


def get_salt():
    """Helper method to get a salt.

    It is recommended that the the salt-size matches the key-size.
    """
    return os.urandom(KEY_LENGTH)


def derive_encryption_key(salt, password):
    """Get the real encryption key.

    Don't use the password directly but derive a encryption key
    dynamically based on the password and a stored key.
    """
    backend = default_backend()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=force_bytes(salt),
        iterations=settings.KEYBAR_KDF_ITERATIONS,
        backend=backend
    )

    key = kdf.derive(force_bytes(password))

    return key


def verify_encryption_key(salt, password, key):
    backend = default_backend()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=force_bytes(salt),
        iterations=settings.KEYBAR_KDF_ITERATIONS,
        backend=backend
    )

    kdf.verify(force_bytes(password), key)

    return key


def encrypt(text, password, salt):
    fernet = Fernet(base64.urlsafe_b64encode(derive_encryption_key(salt, password)))
    return fernet.encrypt(force_bytes(text))


def decrypt(text, password, salt):
    fernet = Fernet(base64.urlsafe_b64encode(derive_encryption_key(salt, password)))
    return force_bytes(fernet.decrypt(force_bytes(text)))


def prettify_fingerprint(fingerprint):
    """
    Returns the fingerprint in its common pretty form::
        XXXX XXXX XXXX XXXX XXXX  XXXX XXXX XXXX XXXX XXXX
    """
    if fingerprint is None:
        return 'NO FINGERPRINT'
    chunks = [fingerprint[i:i + 4] for i in range(0, 32, 4)]
    return '%s  %s' % (' '.join(chunks[0:4]), ' '.join(chunks[4:8]))


def get_server_context(verify=True):
    """Our TLS configuration for the server"""
    server_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

    server_ctx.set_ecdh_curve('prime256v1')
    server_ctx.verify_mode = ssl.CERT_OPTIONAL if not verify else ssl.CERT_REQUIRED

    # This list is based on the official supported ciphers by CloudFlare
    # (cloudflare/sslconfig on GitHub) but is again just a tiny little bit
    # more restricted as we force best security available.
    server_ctx.set_ciphers('EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256')

    # Disable that is not TSL 1.2, explicit is better than implicit
    server_ctx.options |= ssl.OP_NO_SSLv2
    server_ctx.options |= ssl.OP_NO_SSLv3
    server_ctx.options |= ssl.OP_NO_TLSv1
    server_ctx.options |= ssl.OP_NO_TLSv1_1

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

    # Disable that is not TSL 1.2, explicit is better than implicit
    client_ctx.options |= ssl.OP_NO_SSLv2
    client_ctx.options |= ssl.OP_NO_SSLv3
    client_ctx.options |= ssl.OP_NO_TLSv1
    client_ctx.options |= ssl.OP_NO_TLSv1_1

    # Load the certificates
    client_ctx.load_cert_chain(
        settings.KEYBAR_CLIENT_CERTIFICATE,
        settings.KEYBAR_CLIENT_KEY
    )

    client_ctx.load_verify_locations(settings.KEYBAR_CA_BUNDLE)

    return client_ctx
