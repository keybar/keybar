import os

from keybar.conf.base import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'keybar_dev',
    }
}


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''  # noqa
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''


LOGGING['loggers']['root']['level'] = 'DEBUG'
LOGGING['loggers']['celery']['level'] = 'DEBUG'
LOGGING['loggers']['keybar']['level'] = 'DEBUG'

certificates_dir = os.path.join(PROJECT_DIR, 'extras', 'certificates')

KEYBAR_SERVER_CERTIFICATE = os.path.join(certificates_dir, 'server.crt')
KEYBAR_SERVER_KEY = os.path.join(certificates_dir, 'server.key')

KEYBAR_CLIENT_CERTIFICATE = os.path.join(certificates_dir, 'ca.crt')
KEYBAR_CLIENT_KEY = os.path.join(certificates_dir, 'ca.key')

KEYBAR_CA_BUNDLE = os.path.join(certificates_dir, 'ca.db.certs', '01.pem')

# TODO: Make this a bit more automated.
KEYBAR_DOMAIN = 'keybar.local'
KEYBAR_HOST = 'keybar.local:8443'
