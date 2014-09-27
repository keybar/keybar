from itertools import cycle

import ssl
from django.conf import settings


# Verify we can use all feature we require.
assert ssl.HAS_ECDH
assert ssl.HAS_SNI


def xor_strings(string, key):
    assert isinstance(string, (bytes, bytearray))
    assert isinstance(key, (bytes, bytearray))

    base = bytearray(string)

    return bytearray(char ^ k for char, k in zip(base, cycle(key)))


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
