from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedActionLinkRouterMixin


class KeybarApiRouter(ExtendedActionLinkRouterMixin, DefaultRouter):
    pass
