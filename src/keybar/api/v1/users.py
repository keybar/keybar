from rest_framework import generics

from keybar.models.user import User
from keybar.serializers.user import UserSerializer


class ListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
