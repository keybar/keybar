from rest_framework import serializers
from rest_framework.response import Response

from allauth.account.forms import SignupForm
from keybar.api.auth import KeybarNoAuthorizedDeviceApiSignatureAuthentication
from keybar.api.base import Endpoint, ListEndpoint
from keybar.models.user import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'date_joined')


class UserEndpoint(Endpoint):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListEndpoint(UserEndpoint, ListEndpoint):
    pass


class UserRegisterEndpoint(UserEndpoint):
    """Endpoint to register a new user.

    This explicitly is a new endpoint because it's unauthenticated.

    TODO:

     * Take email verification into account
    """
    authentication_classes = (KeybarNoAuthorizedDeviceApiSignatureAuthentication,)
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        form = SignupForm(request.data)

        if form.is_valid():
            user = form.save(request)
            device = request.successful_authenticator.get_device(request)
            device.user = user
            # TODO: Implement TOTP here
            device.authorized = True
            device.save()
            return Response(self.serializer_class(user).data)
        else:
            return Response(form.errors)
