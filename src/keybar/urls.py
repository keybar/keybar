from django.contrib import admin
from django.conf.urls import url, include, patterns

from keybar.web import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(),
        name='keybar-index'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Hookup our REST Api
    url(r'^api/v1/', include('keybar.api.v1.urls', namespace='api-v1')),
)
