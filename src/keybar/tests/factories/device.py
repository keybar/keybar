import factory
from django.contrib.auth.hashers import make_password

from keybar.models.device import Device
from keybar.tests.factories.user import UserFactory


class DeviceFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

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
