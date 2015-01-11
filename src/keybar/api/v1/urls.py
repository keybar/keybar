from django.conf.urls import url, include

from keybar.api import endpoints


urlpatterns = [
    url(r'^users/(?P<pk>.+)/$',
        endpoints.UserEndpoint.as_view(),
        name='keybar-api-user'),

    url(r'^',
        endpoints.CatchallEndpoint.as_view(),
        name='keybar-api-catchall'),
]
