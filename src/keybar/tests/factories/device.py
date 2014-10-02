import factory
from django.contrib.auth.hashers import make_password

from keybar.models.device import Device


class DeviceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Device
