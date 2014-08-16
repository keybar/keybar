import os
import base64
import hashlib

from django.conf import settings
from django.db import models
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

from keybar.utils.crypto import xor_strings


def pbkdf2(salt, password):
    return hashlib.pbkdf2_hmac(
        'sha256',
        salt,
        password,
        settings.KEYBAR_KDF_ITERATIONS)


class Entry(models.Model):

    title = models.CharField(max_length=256, blank=True, default='')
    description = models.TextField(blank=True)

    # Is max_length=256 sufficient?
    username = models.CharField(max_length=256)
    value = models.TextField()

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
        salt = os.urandom(4)
        hashed_value = pbkdf2(salt, password)

        # Ordering of the xor-arguments is important, because of
        # very simplified xor-implementation.
        visible_key = xor_strings(fernet_key, hashed_value)

        return salt + b'$' + visible_key

    def get_encryption_key(self, password):
        salt, visible_key = bytes(self.key).split(b'$', 1)
        hashed_value = pbkdf2(salt, password)

        # Ordering of the xor-arguments is important, because of
        # very simplified xor-implementation.
        return xor_strings(visible_key, hashed_value)
