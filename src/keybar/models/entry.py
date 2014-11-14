from django.db import models
from django.utils.translation import ugettext_lazy as _

from keybar.utils.crypto import encrypt, get_salt


class Entry(models.Model):
    created_by = models.ForeignKey('keybar.User')
    title = models.TextField(_('Title'), blank=True, default='')
    url = models.URLField(blank=True, default='')

    identifier = models.TextField(_('Identifier for login'),
        help_text=_('Usually a username or email address'))
    value = models.TextField(_('The encrypted value for the entry.'),
        help_text=_('Usually a password.'))

    description = models.TextField(_('Description'), blank=True, default='')

    salt = models.BinaryField(null=True, blank=True)

    def set_value(self, password, value, salt=None):
        if salt is None:
            salt = get_salt()

        self.value = encrypt(value, password, salt)
        self.salt = salt
