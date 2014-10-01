import os
import hashlib

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cryptography.fernet import Fernet

from keybar.utils.crypto import xor_strings


def pbkdf2(salt, password):
    return hashlib.pbkdf2_hmac(
        'sha256',
        salt,
        password,
        settings.KEYBAR_KDF_ITERATIONS)


class Entry(models.Model):
    title = models.TextField(_('Title'), blank=True, default='')
    description = models.TextField(_('Description'), blank=True, default='')

    identifier = models.TextField(_('Identifier for login'),
        help_text=_('Usually a username or email address'))
    value = models.TextField(_('The value for the entry.'),
        help_text=_('Usually a password.'))

    # Those parts ar for encrypting/decrypting the stored values
    # The values are stored as 16-byte-salt$key where `key`
    # can be used to obtain the actual encryption key.
    key = models.BinaryField()

    @classmethod
    def derive_encryption_key_spec(cls, password):
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

    def get_encryption_key(self, password):
        # We must split only once. The Fernet key can also contain
        # `$` characters
        salt, visible_key = bytes(self.key).split(b'$', 1)
        hashed_value = pbkdf2(salt, password)

        # Ordering of the xor-arguments is important, because of
        # very simplified xor-implementation.
        return xor_strings(visible_key, hashed_value)
