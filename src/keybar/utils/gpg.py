import os

import gnupg

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils.encoding import force_text, force_bytes


if not os.access(settings.GPG_BIN, os.X_OK):
    raise ImproperlyConfigured(
        'Cannot find GnuPG binary at {}'.format(settings.GPG_BIN)
    )


def encrypt(raw_data, recipients):
    gpg = gnupg.GPG(gnupghome=settings.GPG_HOME, gpgbinary=settings.GPG_BIN)

    encrypted = gpg.encrypt(
        force_bytes(raw_data),
        recipients,
        always_trust=True,
        armor=True)

    return force_text(encrypted)


def decrypt(encrypted_data, passphrase=None):
    gpg = gnupg.GPG(gnupghome=settings.GPG_HOME, gpgbinary=settings.GPG_BIN)

    kwargs = {}

    if passphrase:
        kwargs['passphrase'] = passphrase

    decrypted = gpg.decrypt(force_bytes(encrypted_data), **kwargs)
    return force_text(decrypted.data)
