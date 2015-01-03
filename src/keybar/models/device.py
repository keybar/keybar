# -*- coding: utf-8 -*-
"""
    keybar.models.device
    ~~~~~~~~~~~~~~~~~~~~

    Device model.
"""
import hashlib

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_bytes

from keybar.utils.crypto import prettify_fingerprint
from keybar.utils.db.uuid import UUIDField


class Device(models.Model):
    """A device is a uuid-typed identifier that can be optionally named.

    The idea behind this is that you will be able to restrict access
    to specific devices or even block those in case of burglary.

    This actually requires a client to be easily identified. For this
    each client is requested to get a initial device-id for the very
    first request.
    """
    id = UUIDField(auto=True, primary_key=True)
    user = models.ForeignKey('keybar.User', related_name='devices')
    name = models.TextField(_('Device name'), blank=True, default='')

    public_key = models.TextField(_('Device Public Key'), blank=False)

    # `None` specifies that the user did not yet authorize the device.
    # `False` specifies that the user explicitly deauthorized the device.
    # `True` specifies that the user authorized the device to access his data.
    authorized = models.NullBooleanField(_('Authorized?'), default=None)

    @property
    def fingerprint(self):
        digest = hashlib.md5(force_bytes(self.public_key)).hexdigest()
        return prettify_fingerprint(digest)
