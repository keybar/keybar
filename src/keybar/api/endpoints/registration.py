from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from keybar.api.serializers.registration import RegisterSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save()
