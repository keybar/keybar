from django.conf.urls import url

from keybar.api import endpoints


urlpatterns = [
    url(r'^users/$',
        endpoints.UserListEndpoint.as_view(),
        name='keybar-api-user-list'),
    url(r'^users/register/$',
        endpoints.UserRegisterEndpoint.as_view(),
        name='keybar-api-user-register'),
    url(r'^users/(?P<pk>.+)/$',
        endpoints.UserEndpoint.as_view(),
        name='keybar-api-user'),

    url(r'^',
        endpoints.CatchallEndpoint.as_view(),
        name='keybar-api-catchall'),
]
