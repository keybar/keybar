from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _


class AccessMixin:
    login_url = None
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth
    message = None

    def get_login_url(self):
        """Override this method to customize the login_url."""
        login_url = self.login_url or settings.LOGIN_URL
        return force_text(login_url)

    def get_redirect_field_name(self):
        """Override this method to customize the redirect_field_name."""
        return self.redirect_field_name


class LoginRequiredMixin(AccessMixin):
    """View mixin which verifies that the user is authenticated."""
    message = _('Please authenticate to access this view.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            if self.message:
                messages.error(request, self.message)
            return redirect_to_login(
                request.get_full_path(),
                self.get_login_url(),
                self.get_redirect_field_name())

        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
