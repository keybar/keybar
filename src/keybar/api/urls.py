from django.conf.urls import url

from .endpoints.dummy import AuthenticatedDummyView
from .endpoints.registration import RegisterView

urlpatterns = [
    url(r'auth/register/$', RegisterView.as_view(), name='register'),

    # Dummy view, used for testing.
    url(r'dummy/$', AuthenticatedDummyView.as_view()),
]
