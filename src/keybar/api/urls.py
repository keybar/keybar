from django.conf.urls import url

from .endpoints.dummy import AuthenticatedDummyEndpoint


urlpatterns = [
    url(r'dummy/$', AuthenticatedDummyEndpoint.as_view())
]
