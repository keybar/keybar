from django.db import models
from django.utils.translation import ugettext_lazy as _


class Entry(models.Model):
    title = models.TextField(_('Title'), blank=True, default='')
    description = models.TextField(_('Description'), blank=True, default='')

    identifier = models.TextField(_('Identifier for login'),
        help_text=_('Usually a username or email address'))
    value = models.TextField(_('The encrypted value for the entry.'),
        help_text=_('Usually a password.'))

    # Those parts are for encrypting/decrypting the stored values
    # The values are stored as 16-byte-salt$key where `key`
    # can be used to obtain the actual encryption key.
    key = models.BinaryField()
