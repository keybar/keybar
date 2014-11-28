# -*- coding: utf-8 -*-
"""
    keybar.models.user
    ~~~~~~~~~~~~~~~~~~

    User model.
"""
import os

from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, UserManager

from keybar.core.tasks import send_mail_async


class User(AbstractBaseUser):
    email = models.EmailField(_('Email'), max_length=254, unique=True)
    name = models.TextField(_('Name'), max_length=100, blank=True, null=True)
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # Required for django-admin
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_superuser = models.BooleanField(
        _('superuser status'), default=False,
        help_text=_('Designates that this user has all permissions without '
                    'explicitly assigning them.'))

    # TODO: find a way to encrypt this :/
    totp_secret = models.BinaryField()

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.totp_secret:
            self.totp_secret = os.urandom(30)
        return super(User, self).save(*args, **kwargs)

    def has_module_perms(self, app_label):
        return self.is_superuser

    def has_perm(self, app_label):
        return self.is_superuser

    def send_mail(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""
        send_mail_async.delay(subject, message, from_email, [self.email],
                              **kwargs)

    def get_absolute_url(self):
        return reverse('keybar-profile', kwargs={'email': self.email})

    def get_display_name(self):
        return self.name or self.email

    def get_short_name(self):
        return self.get_display_name()
