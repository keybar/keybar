from rest_framework_httpsignature.authentication import SignatureAuthentication

from keybar.models.user import User


class KeybarApiSignatureAuthentication(SignatureAuthentication):
    API_KEY_HEADER = 'X-Api-Key'

    def fetch_user_data(self, api_key):
        try:
            user = User.objects.get(api_key=api_key)
            return (user, 'my secret string')
        except User.DoesNotExist:
            return None
