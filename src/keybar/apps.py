from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class KeybarConfig(AppConfig):
    name = 'keybar'
    verbose_name = _('Keybar')

    def ready(self):
        from keybar.models import user, entry, device, organization, team  # noqa
