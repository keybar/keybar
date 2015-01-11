from rest_framework_extensions.decorators import link

from keybar.api.base import Endpoint
from keybar.models.user import User
from keybar.serializers.user import UserSerializer


class UserEndpoint(Endpoint):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @link()
    def test(self, request, pk=None):
        return Response(['test'])
