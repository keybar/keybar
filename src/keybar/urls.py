from django.contrib import admin
from django.conf.urls import url, include, patterns

from keybar.web import views


urlpatterns = patterns('',
    url(r'^$',
        views.IndexView.as_view(),
        name='keybar-index'),
    url(r'^vault/$',
        views.VaultView.as_view(),
        name='keybar-vault'),
    url(r'^entry/$',
        views.EntryAddFormView.as_view(),
        name='keybar-entry-new'),
    url(r'^entry/(?P<pk>.+)/edit/$',
        views.EntryUpdateFormView.as_view(),
        name='keybar-entry-edit'),
    url(r'^entry/(?P<pk>.+)/$',
        views.EntryDetailFormView.as_view(),
        name='keybar-entry'),
    url(r'totp-qrcode.png$',
        views.TotpQrCodeView.as_view(),
        name='keybar-totp-qrcode'),


    url(r'^accounts/', include('allauth.urls')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Hookup our REST Api
    url(r'^api/v1/', include('keybar.api.v1.urls', namespace='api-v1')),

    url(r'^api/docs/', include('rest_framework.urls', namespace='rest_framework'))
)
