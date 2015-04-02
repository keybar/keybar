import os
import base64
import uuid

from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from keybar.models.device import Device
from keybar.utils.crypto import encrypt, decrypt, get_salt
from keybar.utils.db.json import JSONField


class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    owner = models.ForeignKey('keybar.User')
    title = models.TextField(_('Title'), blank=True, default='')
    url = models.URLField(blank=True, default='')

    identifier = models.TextField(_('Identifier for login'),
        help_text=_('Usually a username or email address'))
    value = models.BinaryField(_('The encrypted value for the entry.'),
        help_text=_('Usually a password.'))

    description = models.TextField(_('Description'), blank=True, default='')

    tags = ArrayField(models.TextField(blank=True), blank=True, null=True)

    salt = models.BinaryField(null=True, blank=True)

    keys = JSONField(default={})

    log = JSONField(default={})

    force_two_factor_authorization = models.BooleanField(default=False)

    @classmethod
    def create(cls, device_id, value, private_key, **kwargs):
        salt = get_salt()
        master_key = os.urandom(32)

        device = Device.objects.get(pk=device_id)
        device_key = device.loaded_public_key.encrypt(master_key, 32)[0]

        encrypted_value = encrypt(value, master_key, salt)
        keys = {device.id.hex: force_text(base64.b64encode(device_key))}

        return cls.objects.create(salt=salt, keys=keys, value=encrypted_value, **kwargs)

    def update(self, value, private_key):
        if not self.keys:
            raise ValueError('Please use Entry.create to create an initial entry')

        salt = get_salt()

        # TODO: This might not be efficient, use id? I actually like the idea
        # of associating the device directly via the private key
        # TODO: This whole API and process kinda seems unreasonable.... :-/
        # Somehow I think I need to regenerate the master-key and
        # update all related device keys. Since I have the public-key I
        # should be able to do that.

        device = Device.objects.get(public_key=private_key.publickey().exportKey('PEM'))
        device_key = base64.b64decode(self.keys[device.id.hex])

        master_key = private_key.decrypt(device_key)

        self.value = encrypt(value, master_key, salt)
        self.salt = salt

    @classmethod
    def decrypt(cls, entry_id, device_id, private_key):
        entry = cls.objects.get(pk=entry_id)
        device = Device.objects.get(id=device_id)

        device_key = base64.b64decode(entry.keys[device.id.hex])

        return decrypt(entry.value, private_key.decrypt(device_key), entry.salt)

    def __str__(self):
        if self.url and self.title:
            return '{0} ({1})'.format(self.title, self.url)
        elif self.url:
            return self.url
        elif self.title:
            return self.title
        else:
            return self.identifier
