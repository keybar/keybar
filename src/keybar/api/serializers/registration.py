from django.contrib.auth import password_validation
from rest_framework import serializers

from keybar.models.user import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
