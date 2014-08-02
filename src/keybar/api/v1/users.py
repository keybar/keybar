from rest_framework import generics
from rest_framework.response import Response

from keybar.models.user import User
from keybar.serializers.user import UserSerializer


class ListView(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer
