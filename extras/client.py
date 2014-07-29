import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keybar.settings')

# import os
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.hazmat.backends import default_backend
# backend = default_backend()
# salt = os.urandom(16)
# # derive
# kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt=salt,
#     iterations=100000,
#     backend=backend
# )

# key = kdf.derive(b"my great password")
# print(key)

# # verify
# kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt=salt,
#     iterations=100000,
#     backend=backend
# )

# print(kdf.verify(b"my great password", key))

import requests
from django.conf import settings
from http_signature.requests_auth import HTTPSignatureAuth

API_KEY_ID = '418a3fdbd04b4ee2833d6cfd3a122c2c'
SECRET = 'my secret string'

signature_headers = ['request-line', 'accept', 'date', 'host']
headers = {
    'Host': 'keybar.local:8443',
    'Accept': 'application/json',
    'X-Api-Key': API_KEY_ID,
}

auth = HTTPSignatureAuth(key_id=API_KEY_ID, secret=SECRET,
                         algorithm='hmac-sha256',
                         headers=signature_headers)

response = requests.get('https://keybar.local:8443/api/users/',
                   auth=auth, headers=headers,
                   verify=settings.KEYBAR_CA_BUNDLE)

print(response.content)
