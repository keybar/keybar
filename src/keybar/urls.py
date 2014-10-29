from django.contrib import admin
from django.conf.urls import url, include, patterns

from keybar.web import views


urlpatterns = patterns('',
    url(r'^$',
        views.IndexView.as_view(),
        name='keybar-index'),
    url(r'^register/$',
        views.RegisterView.as_view(),
        name='keybar-register'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Hookup our REST Api
    url(r'^api/v1/', include('keybar.api.v1.urls', namespace='api-v1')),

    url(r'^api/docs/', include('rest_framework.urls', namespace='rest_framework'))
)
