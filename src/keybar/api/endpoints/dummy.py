import json

from rest_framework import views
from rest_framework.response import Response


class AuthenticatedDummyView(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response(json.dumps({'dummy': 'ok'}))
