# -*- coding: utf-8 -*-
"""
    keybar.models.device
    ~~~~~~~~~~~~~~~~~~~~

    Device model.
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuidfield import UUIDField


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
