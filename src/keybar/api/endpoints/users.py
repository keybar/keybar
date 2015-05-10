from allauth.account.forms import SignupForm
from rest_framework.response import Response

from keybar.api.base import Endpoint, ListEndpoint
from keybar.models.user import User
from keybar.serializers.user import UserSerializer


class UserEndpoint(Endpoint):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListEndpoint(UserEndpoint, ListEndpoint):
    pass


class UserRegisterEndpoint(UserEndpoint):
    """Endpoint to register a new user.

    TODO:

     * Take email verification into account
    """
    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        form = SignupForm(request.data)

        if form.is_valid():
            user = form.save(request)
            return Response(self.serializer_class(user).data)
        else:
            return Response(form.errors)
