from django.contrib.auth import password_validation
from rest_framework import serializers

from keybar.models.user import User
from keybar.models.device import Device
from keybar.utils.crypto import load_public_key


class RegisterSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(max_length=256, required=False)
    public_key = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'device_name', 'public_key')

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    def validate_public_key(self, public_key):
        try:
            loaded = load_public_key(public_key)
        except ValueError:
            raise serializers.ValidationError('Invalid public key')

        return public_key

    def create(self, validated_data):
        password = validated_data.pop('password')
        public_key = validated_data.pop('public_key')
        device_name = validated_data.pop('device_name', '')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        Device.objects.create(
            public_key=public_key,
            name=device_name,
            user=user,
            authorized=True)
        return user
