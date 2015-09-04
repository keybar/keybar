import base64
import os

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from keybar.models.device import Device
from keybar.utils.crypto import (
    fernet_decrypt, fernet_encrypt, get_salt, private_key_decrypt, public_key_encrypt)
from keybar.utils.db import KeybarModel, sane_repr
from keybar.utils.db.json import JSONField


class Entry(KeybarModel):
    vault = models.ForeignKey('keybar.Vault', related_name='entries')

    title = models.TextField(_('Title'), blank=True, default='')
    url = models.URLField(blank=True, default='')

    identifier = models.TextField(_('Identifier for login'),
        help_text=_('Usually a username or email address'),
        blank=True)

    values = JSONField(default={})

    description = models.TextField(_('Description'), blank=True, default='')

    tags = ArrayField(models.TextField(blank=True), blank=True, null=True)

    salt = models.BinaryField(null=True, blank=True)

    keys = JSONField(default={})

    log = JSONField(default={})

    enable_two_factor_authorization = models.BooleanField(default=False)

    __repr__ = sane_repr('id', 'identifier')

    @classmethod
    def create(cls, device_id, values, **kwargs):
        """Create a new entry.

        This generates a master key and encrypts it with the public key
        from the device from which the new entry get's created.

        The master key is used to encrypt the values.

        The master key is never stored.
        """
        salt = get_salt()
        master_key = os.urandom(32)

        device = Device.objects.get(pk=device_id)
        device_key = public_key_encrypt(device.loaded_public_key, master_key)

        encrypted = {
            key: fernet_encrypt(value, master_key, salt)
            for key, value in values.items()}

        keys = {device.id.hex: force_text(base64.b64encode(device_key))}

        return cls.objects.create(salt=salt, keys=keys, values=encrypted, **kwargs)

    def decrypt(self, key, device, private_key):
        """Decrypt the specific key on this entry for a specific device.

        ... note::

            This is only used for cloud-stored passwords so the code
            can reside here in the model.

            Each client must implement this functionality itself.
        """
        device_key = base64.b64decode(self.keys[device.id.hex])

        return fernet_decrypt(
            self.values[key],
            private_key_decrypt(private_key, device_key),
            self.salt)

    def __str__(self):
        if self.url and self.title:
            return '{0} ({1})'.format(self.title, self.url)
        elif self.url:
            return self.url
        elif self.title:
            return self.title
        else:
            return self.identifier
