from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedActionLinkRouterMixin

from keybar.api.v1 import users


class Router(ExtendedActionLinkRouterMixin, DefaultRouter):
    pass


router = Router()
router.register('users', users.UserViewSet)

urlpatterns = [
    # Hookup our REST Api
    url(r'^', include(router.urls)),
]
