from django.conf.urls import include, url
from django.contrib import admin

from keybar.web import views


urlpatterns = [
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
    url(r'setup-totp/$',
        views.SetupTotpView.as_view(),
        name='keybar-setup-totp'),
    url(r'^tags/$',
        views.TagsView.as_view(),
        name='keybar-tags'),

    url(r'^account/', include('allauth.urls')),

    url(r'account/sessions/$', views.SessionListView.as_view(),
        name='keybar-account-session-list'),
    url(r'account/sessions/delete/(?P<pk>.+)/$', views.SessionDeleteView.as_view(),
        name='keybar-account-session-delete'),

    # Hookup our REST Api
    url(r'^api/', include('keybar.api.urls', namespace='keybar-api')),
    url(r'^api/docs/', include('rest_framework.urls', namespace='rest_framework')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
]
