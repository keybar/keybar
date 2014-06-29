from django.conf import settings
import os
import os.path


def pytest_configure(config):
    if not settings.configured:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'keybar.conf.test'

    test_db = os.environ.get('DB', 'sqlite')
    if test_db == 'mysql':
        settings.DATABASES['default'].update({
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'keybar_test',
            'USER': 'root',
        })
    elif test_db == 'postgres':
        settings.DATABASES['default'].update({
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'postgres',
            'NAME': 'keybar_test',
        })
    elif test_db == 'sqlite':
        settings.DATABASES['default'].update({
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        })

    # override a few things with our test specifics
    settings.INSTALLED_APPS = tuple(settings.INSTALLED_APPS) + (
        'keybar.tests',
    )
