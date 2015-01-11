import os

import factory
from Crypto.PublicKey import RSA
from django.conf import settings

from keybar.models.device import Device
from keybar.tests.factories.user import UserFactory


public_fpath = os.path.join(
    settings.BASE_DIR, 'tests', 'resources', 'rsa_keys', 'id_rsa.pub')
private_fpath = os.path.join(
    settings.BASE_DIR, 'tests', 'resources', 'rsa_keys', 'id_rsa')


with open(public_fpath, 'rb') as fobj:
    PUBLIC_KEY = RSA.importKey(fobj.read())


with open(private_fpath, 'rb') as fobj:
    PRIVATE_KEY = RSA.importKey(fobj.read())


class DeviceFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    public_key = PUBLIC_KEY.exportKey('PEM')

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
