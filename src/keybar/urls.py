from django.contrib import admin
from django.conf.urls import url, include, patterns

from keybar.web import api, views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(),
        name='keybar-index'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Hookup our REST Api
    url(r'^api/users/', api.ListUsersView.as_view())
)
