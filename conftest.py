import os.path
import os

import pytest
from django.conf import settings
from pytest_django.lazy_django import skip_if_no_django


def pytest_configure(config):
    if not settings.configured:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'keybar.conf.test'

    # override a few things with our test specifics
    settings.INSTALLED_APPS = tuple(settings.INSTALLED_APPS) + (
        'keybar.tests',
    )


@pytest.fixture(scope='session')
def keybar_liveserver(request):
    skip_if_no_django()

    from keybar.tests.helpers import LiveServer

    addr = request.config.getvalue('liveserver')

    if not addr:
        addr = os.getenv('DJANGO_TEST_LIVE_SERVER_ADDRESS')
    if not addr:
        addr = 'keybar.local:8081,8100-8200'

    server = LiveServer(addr)
    request.addfinalizer(server.stop)

    return server
