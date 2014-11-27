import os

from keybar.conf.base import *

certificates_dir = os.path.join(PROJECT_DIR, 'extras', 'certificates')

KEYBAR_SERVER_CERTIFICATE = os.path.join(certificates_dir, 'server.crt')
KEYBAR_SERVER_KEY = os.path.join(certificates_dir, 'server.key')

KEYBAR_CLIENT_CERTIFICATE = os.path.join(certificates_dir, 'ca.crt')
KEYBAR_CLIENT_KEY = os.path.join(certificates_dir, 'ca.key')

KEYBAR_CA_BUNDLE = os.path.join(certificates_dir, 'ca.db.certs', '01.pem')

# TODO: Make this a bit more automated.
KEYBAR_DOMAIN = 'keybar.local'
KEYBAR_HOST = 'keybar.local:8443'
