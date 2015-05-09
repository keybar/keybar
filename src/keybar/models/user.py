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
from django.contrib.auth.models import AbstractBaseUser, UserManager as BaseUserManager

from keybar.tasks.mail import send_mail_async
from keybar.utils.avatar import get_profile_image
from keybar.utils.db import KeybarModel


class UserManager(BaseUserManager):
    """Compatibility layer for our email-only api."""

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email, is_staff=is_staff, is_active=True,
            is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(KeybarModel, AbstractBaseUser):
    email = models.EmailField(_('Email'), unique=True)
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

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_superuser

    def has_perm(self, app_label):
        return self.is_superuser

    def send_mail(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""
        send_mail_async.delay(
            subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        return reverse('keybar-profile', kwargs={'email': self.email})

    def get_display_name(self):
        return self.name or self.email

    def get_short_name(self):
        return self.get_display_name()

    @property
    def profile_image(self):
        return get_profile_image(self)
