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

print(requests.get(
    'https://keybar.local:8443',
    verify=settings.KEYBAR_CA_BUNDLE))
