import os.path
import os

import pytest
from django.conf import settings as django_settings
from pytest_django.lazy_django import skip_if_no_django


def pytest_configure(config):
    if not django_settings.configured:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keybar.conf.test')

    # override a few things with our test specifics
    django_settings.INSTALLED_APPS = tuple(django_settings.INSTALLED_APPS) + (
        'keybar.tests',
    )


@pytest.fixture(scope='session')
def keybar_liveserver(request, autouse=True):
    skip_if_no_django()

    from keybar.tests.helpers import LiveServer

    addr = request.config.getvalue('liveserver')

    server = LiveServer('keybar.local:9999')
    request.addfinalizer(server.stop)

    return server
