import os

from keybar.conf.base import *


certificates_dir = os.path.join(BASE_DIR, 'tests', 'resources', 'certificates')

KEYBAR_SERVER_CERTIFICATE = os.path.join(certificates_dir, 'KEYBAR-intermediate-SERVER.cert')
KEYBAR_SERVER_KEY = os.path.join(certificates_dir, 'KEYBAR-intermediate-SERVER.key')

KEYBAR_CLIENT_CERTIFICATE = os.path.join(certificates_dir, 'KEYBAR-intermediate-CLIENT.cert')
KEYBAR_CLIENT_KEY = os.path.join(certificates_dir, 'KEYBAR-intermediate-CLIENT.key')

KEYBAR_CA_BUNDLE = os.path.join(certificates_dir, 'KEYBAR-ca-bundle.crt')

# TODO: Make this a bit more automated.
KEYBAR_DOMAIN = 'keybar.local'
KEYBAR_HOST = 'keybar.local:8443'

KEYBAR_VERIFY_CLIENT_CERTIFICATE = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
