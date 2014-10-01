from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class KeybarConfig(AppConfig):
    name = 'keybar'
    verbose_name = _('Keybar')

    def ready(self):
        # We do like our application structure more than django's
        # so we import our modules manually.
        from keybar.models import user, entry, device # noqa
