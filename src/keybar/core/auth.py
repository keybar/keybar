import os
from rest_framework_httpsignature.authentication import SignatureAuthentication
from django.conf import settings

from keybar.models.user import User


class KeybarApiSignatureAuthentication(SignatureAuthentication):
    API_KEY_HEADER = 'X-Api-Key'

    def fetch_user_data(self, api_key):
        try:
            user = User.objects.get(api_key=api_key)
            fpath = os.path.join(
                settings.PROJECT_DIR, 'extras', 'example_keys', 'private_key.pem')

            with open(fpath, 'rb') as fobj:
                secret = fobj.read()

            return (user, secret)
        except User.DoesNotExist:
            return (None, None)
