import json

from rest_framework.test import APIClient as BaseAPIClient

from keybar.models.device import Device
from keybar.utils.jwt import encode_token


class APIClient(BaseAPIClient):
    """
    Subclass to handle our custom accept headers required
    for proper versioning and data parsing.

    Requires a test-user with the following credentials to be setup in
    case of using an authenticated endpoint:

    * E-mail: test@test.test
    * Password: test123456
    """
    content_type = 'application/vnd.keybar+json'
    default_format = 'json'

    def __init__(self, *args, **kwargs):
        self.device_id = kwargs.pop('device_id', None)
        super().__init__(*args, **kwargs)

    def generic(self, method, path, data='', content_type=None, secure=False, **extra):
        extra.update({
            'HTTP_HOST': 'testserver',
            'HTTP_ACCEPT': self.content_type,
        })

        if extra.get('authorized', False):
            device = Device.objects.get(pk=self.device_id)
            token = encode_token(device.id, device.public_key)
            extra['HTTP_AUTHORIZATION'] = 'JWT {}'.format(token)

        return super().generic(method, path, data, self.content_type, secure, **extra)

    def _parse_json(self, response, **extra):
        content_type = response.get('Content-Type')
        types = ('application/json', self.content_type)

        if not any(type in content_type for type in types):
            raise ValueError(
                'Content-Type header is "{0}", not "application/json"'
                .format(response.get('Content-Type'))
            )

        return json.loads(response.content.decode(), **extra)
