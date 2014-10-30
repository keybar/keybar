from rest_framework import serializers

from keybar.models.user import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'date_joined')
