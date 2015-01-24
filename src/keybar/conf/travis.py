import os
from keybar.conf.test import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['KEYBAR_TEST_DB_NAME'],
        'USER': os.environ['KEYBAR_TEST_DB_USER']
    }
}
