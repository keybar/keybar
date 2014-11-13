import os

import factory
from django.conf import settings
from django.contrib.auth.hashers import make_password

from keybar.models.device import Device
from keybar.tests.factories.user import UserFactory


fpath = os.path.join(settings.PROJECT_DIR, 'extras', 'example_keys', 'id_rsa.pub')

with open(fpath, 'rb') as fobj:
    PUBLIC_KEY = fobj.read()


class DeviceFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    public_key = PUBLIC_KEY

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
