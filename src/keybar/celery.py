from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "keybar.settings")

from django.conf import settings

celery = Celery('keybar')

celery.config_from_object('django.conf:settings')
celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
