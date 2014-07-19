import ssl
from django.conf import settings


# Verify we can use all feature we require.
assert ssl.HAS_ECDH
assert ssl.HAS_SNI


def get_server_context():
    """Our TLS configuration for the server"""
    server_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    server_ctx.set_ecdh_curve('prime256v1')
    server_ctx.verify_mode = ssl.CERT_REQUIRED

    # ECDHE appears to be preferred to RSA in many ways
    server_ctx.set_ciphers('ECDHE-ECDSA-AES256-SHA384')

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


def get_client_context():
    """Matching TLS configuration for the client."""
    client_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    client_ctx.verify_mode = ssl.CERT_REQUIRED

    # Require checking the hostname
    client_ctx.check_hostname = True

    # ECDHE appears to be preferred to RSA in many ways. Same as the server.
    client_ctx.set_ciphers('ECDHE-ECDSA-AES256-SHA384')

    # Mitigate CRIME
    client_ctx.options |= ssl.OP_NO_COMPRESSION

    # Load the certificates
    client_ctx.load_cert_chain(
        settings.KEYBAR_CLIENT_CERTIFICATE,
        settings.KEYBAR_CLIENT_KEY
    )
