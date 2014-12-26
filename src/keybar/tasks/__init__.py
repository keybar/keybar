import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keybar.settings')

from django.conf import settings

from celery import Celery

celery = Celery('keybar')

celery.config_from_object('django.conf:settings')
celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
