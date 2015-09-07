import base64
import os
import ssl

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings
from django.utils.encoding import force_bytes, force_text


# Verify we can use all feature we require.
assert ssl.HAS_ECDH
assert ssl.HAS_SNI


KEY_LENGTH = 32

# As per https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_configurations
CIPHERS = (
    'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256'
    ':ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384'
    ':DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM'
    ':ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA'
    ':ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384'
    ':ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256'
    ':DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256'
    ':DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA'
    ':!aNULL:!eNULL:!EXPORT:!DES:!RC4:!3DES:!MD5:!PSK'
)


def get_salt():
    """Helper method to get a salt.

    It is recommended that the the salt-size matches the key-size.
    """
    return os.urandom(KEY_LENGTH)


def generate_rsa_keys(key_size=4096):
    private_key = rsa.generate_private_key(
        key_size=key_size,
        public_exponent=65537,
        backend=default_backend())

    return (private_key, private_key.public_key())


def serialize_public_key(public_key):
    return force_text(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo))


def serialize_private_key(private_key, password=None):
    if password is None:
        return force_text(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    assert isinstance(password, bytes)

    return force_text(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    ))


def load_public_key(key):
    """This assumes PEM for now."""
    return serialization.load_pem_public_key(
        force_bytes(key),
        backend=default_backend()
    )


def load_private_key(key, password=None):
    return serialization.load_pem_private_key(
        force_bytes(key),
        password=password,
        backend=default_backend()
    )


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


def fernet_encrypt(text, password, salt):
    """Ecrypts ``text`` with ``password`` and ``salt``.

    :returns: A base64 encoded fernet token"""
    fernet = Fernet(base64.urlsafe_b64encode(derive_encryption_key(salt, password)))
    return force_text(fernet.encrypt(force_bytes(text)))


def fernet_decrypt(text, password, salt):
    fernet = Fernet(base64.urlsafe_b64encode(derive_encryption_key(salt, password)))
    return force_bytes(fernet.decrypt(force_bytes(text)))


def public_key_encrypt(public_key, data):
    try:
        return public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )
    except (AssertionError, ValueError):
        return None


def private_key_decrypt(private_key, data):
    try:
        return private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )
    except (AssertionError, ValueError):
        return None


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
    server_ctx.set_ciphers(CIPHERS)

    # Disable that is not TSL 1.0+
    server_ctx.options |= ssl.OP_NO_SSLv2
    server_ctx.options |= ssl.OP_NO_SSLv3
    server_ctx.options |= ssl.OP_NO_TLSv1

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


# TODO: Unused for now, unfortunately python-requests does not support
# passing in a SSLContext :(
# We do verify the client certificate but a few more options would be
# nice.
def get_client_context(verify=True):
    """Matching TLS configuration for the client."""
    client_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

    client_ctx.verify_mode = ssl.CERT_OPTIONAL if not verify else ssl.CERT_REQUIRED

    # Require checking the hostname
    client_ctx.check_hostname = True

    # Same as the server.
    client_ctx.set_ciphers(CIPHERS)

    # Mitigate CRIME
    client_ctx.options |= ssl.OP_NO_COMPRESSION

    # Disable that is not TSL 1.0+
    client_ctx.options |= ssl.OP_NO_SSLv2
    client_ctx.options |= ssl.OP_NO_SSLv3

    # Load the certificates
    client_ctx.load_cert_chain(
        settings.KEYBAR_CLIENT_CERTIFICATE,
        settings.KEYBAR_CLIENT_KEY
    )

    client_ctx.load_verify_locations(settings.KEYBAR_CA_BUNDLE)

    return client_ctx
