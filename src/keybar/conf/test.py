from keybar.conf.base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'keybar_test',
    }
}

certificates_dir = os.path.join(BASE_DIR, 'tests', 'resources', 'certificates')

KEYBAR_SERVER_CERTIFICATE = os.path.join(certificates_dir, 'KEYBAR-intermediate-SERVER.cert')
KEYBAR_SERVER_KEY = os.path.join(certificates_dir, 'KEYBAR-intermediate-SERVER.key')

KEYBAR_CLIENT_CERTIFICATE = os.path.join(certificates_dir, 'KEYBAR-intermediate-CLIENT.cert')
KEYBAR_CLIENT_KEY = os.path.join(certificates_dir, 'KEYBAR-intermediate-CLIENT.key')

KEYBAR_CA_BUNDLE = os.path.join(certificates_dir, 'KEYBAR-ca-bundle.crt')

KEYBAR_VERIFY_CLIENT_CERTIFICATE = True

KEYBAR_DOMAIN = 'local.keybar.io'
KEYBAR_HOST = 'local.keybar.io:9999'

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

KEYBAR_KDF_ITERATIONS = 100
