import hashlib
import os
import ssl
import json
from email.utils import formatdate
from datetime import datetime
from time import mktime
from base64 import encodebytes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keybar.settings')

import django
django.setup()

from django.conf import settings
from httpsig.requests_auth import HTTPSignatureAuth
import requests

from keybar.models.user import User

secret = open('extras/example_keys/id_rsa', 'rb').read()
user = User.objects.get(username='admin')

signature_headers = ['(request-target)', 'accept', 'date', 'host']

now = datetime.now()
stamp = mktime(now.timetuple())

data = {}
content_md5 = encodebytes(hashlib.md5(json.dumps(data)).digest()).strip()

headers = {
    'Host': 'keybar.local:8443',
    'Method': 'GET',
    'Path': '/api/v1/users/',
    'Accept': 'application/json',
    'X-Device-Id': user.devices.all().first().id.hex,
    'Content-MD5': content_md5,
    'Date': formatdate(timeval=stamp, localtime=False, usegmt=True)
}

auth = HTTPSignatureAuth(
    key_id=user.api_key.hex,
    secret=secret,
    headers=signature_headers,
    algorithm='rsa-sha256')

response = requests.get(
    'https://keybar.local:8443/api/v1/users/',
    auth=auth,
    headers=headers,
    verify=settings.KEYBAR_CA_BUNDLE)

print(response.content)
