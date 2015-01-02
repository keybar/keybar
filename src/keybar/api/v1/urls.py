from django.conf.urls import url, include

from keybar.api import KeybarApiRouter
from keybar.api import users


router = Router()
router.register('users', users.UserViewSet)

urlpatterns = [
    # Hookup our REST Api
    url(r'^', include(router.urls)),
]
