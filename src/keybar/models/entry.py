from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from djorm_pgarray.fields import TextArrayField

from keybar.utils.crypto import encrypt, decrypt, get_salt
from keybar.utils.db.uuid import UUIDField
from keybar.utils.db.json import JSONField


class Entry(models.Model):
    id = UUIDField(auto=True, primary_key=True)

    owner = models.ForeignKey('keybar.User')
    title = models.TextField(_('Title'), blank=True, default='')
    url = models.URLField(blank=True, default='')

    identifier = models.TextField(_('Identifier for login'),
        help_text=_('Usually a username or email address'))
    value = models.BinaryField(_('The encrypted value for the entry.'),
        help_text=_('Usually a password.'))

    description = models.TextField(_('Description'), blank=True, default='')

    tags = TextArrayField(null=True, blank=True)

    salt = models.BinaryField(null=True, blank=True)

    force_two_factor_authorization = models.BooleanField(default=False)

    log = JSONField(default={})

    def set_value(self, password, value, salt=None):
        if salt is None:
            salt = get_salt()

        self.value = encrypt(value, password, salt)
        self.salt = salt

    def decrypt(self, password):
        return force_text(decrypt(self.value, password, self.salt))

    def __str__(self):
        if self.url and self.title:
            return '{0} ({1})'.format(self.title, self.url)
        elif self.url:
            return self.url
        elif self.title:
            return self.title
        else:
            return self.identifier
