from rest_framework import views
from rest_framework.response import Response

from keybar.utils import json


class AuthenticatedDummyEndpoint(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response(json.dumps({'dummy': 'ok'}))
