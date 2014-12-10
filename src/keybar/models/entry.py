from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuidfield import UUIDField
from djorm_pgarray.fields import TextArrayField

from keybar.utils.crypto import encrypt, decrypt, get_salt


class Entry(models.Model):
    id = UUIDField(auto=True, primary_key=True)

    created_by = models.ForeignKey('keybar.User')
    title = models.TextField(_('Title'), blank=True, default='')
    url = models.URLField(blank=True, default='')

    identifier = models.TextField(_('Identifier for login'),
        help_text=_('Usually a username or email address'))
    value = models.BinaryField(_('The encrypted value for the entry.'),
        help_text=_('Usually a password.'))

    description = models.TextField(_('Description'), blank=True, default='')

    tags = TextArrayField(null=False, blank=True, default=[])

    salt = models.BinaryField(null=True, blank=True)

    def set_value(self, password, value, salt=None):
        if salt is None:
            salt = get_salt()

        self.value = encrypt(value, password, salt)
        self.salt = salt

    def decrypt(self, password):
        return decrypt(self.value, password, self.salt)

    def __str__(self):
        if self.url and self.title:
            return '{0} ({1})'.format(self.title, self.url)
        elif self.url:
            return self.url
        elif self.title:
            return self.title
        else:
            return self.identifier
