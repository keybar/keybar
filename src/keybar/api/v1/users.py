from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_extensions.decorators import link

from keybar.models.user import User
from keybar.serializers.user import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @link()
    def test(self, request, pk=None):
        return Response(['test'])
