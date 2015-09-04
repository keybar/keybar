import os

import factory
from django.conf import settings

from keybar.models.device import Device
from keybar.tests.factories.user import UserFactory
from keybar.utils.crypto import load_private_key, serialize_public_key


private_fpath = os.path.join(
    settings.BASE_DIR, 'tests', 'resources', 'rsa_keys', 'id_rsa')


with open(private_fpath, 'rb') as fobj:
    PRIVATE_KEY = load_private_key(fobj.read())
    PUBLIC_KEY = PRIVATE_KEY.public_key()


class DeviceFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    public_key = serialize_public_key(PUBLIC_KEY)

    class Meta:
        model = Device


class AuthorizedDeviceFactory(DeviceFactory):
    authorized = True

    class Meta:
        model = Device


class DeauthorizedDeviceFactory(DeviceFactory):
    authorized = False

    class Meta:
        model = Device
