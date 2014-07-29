# -*- coding: utf-8 -*-
"""
    keybar.models.user
    ~~~~~~~~~~~~~~~~~~

    User model.
"""
from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from uuidfield import UUIDField

from keybar.managers import UserManager


class User(AbstractBaseUser):
    username = models.CharField(_('Username'), max_length=50, null=True, unique=True)
    email = models.EmailField(_('Email'), max_length=254, unique=True)
    name = models.CharField(_('Name'), max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    is_superuser = models.BooleanField(
        _('superuser status'), default=False,
        help_text=_('Designates that this user has all permissions without '
                    'explicitly assigning them.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    email_verified = models.BooleanField(default=False)
    enable_notifications = models.BooleanField(default=False)

    # TODO: implement device-based tokens
    api_key = UUIDField(auto=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        # the admin requires this method
        return self.is_superuser

    def send_mail(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""
        from keybar.tasks import send_mail_async
        send_mail_async.delay(subject, message, from_email, [self.email],
                              **kwargs)

    def get_absolute_url(self):
        return reverse('keybar-profile', kwargs={'email': self.email})

    def get_full_name(self):
        return self.title

    def get_short_name(self):
        "Returns the short name for the user."
        return self.title

    def get_display_name(self):
        return self.title or self.username
