from Crypto.PublicKey import RSA
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db import models

from keybar.api.base import Endpoint
from keybar.models.device import Device


class CreateDeviceSerializer(serializers.ModelSerializer):
    public_key = serializers.ModelField(
        read_only=False,
        model_field=models.CharField()
    )

    class Meta:
        model = Device

    def validate_public_key(self, value):
        try:

            public_key = RSA.importKey(value).exportKey('DER')
        except ValueError:
            raise serializers.ValidationError('Invalid public key.')

        if Device.objects.filter(public_key=public_key).exists():
            raise serializers.ValidationError('Device already exists')

        return public_key


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ('id', 'name',)


class DeviceEndpoint(Endpoint):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceRegisterEndpoint(DeviceEndpoint):
    """Endpoint to register a new device.

    This endpoint is used to register a new device
    so thtat it can be used to create a new user account.

    To accociate a device with a user later on, use the `/users/` endpoint.
    """
    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = CreateDeviceSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            device = serializer.save()
            return Response(self.serializer_class(device).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
