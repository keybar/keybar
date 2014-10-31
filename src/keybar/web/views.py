from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login as auth_login
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from keybar.web.forms import RegisterForm, LoginForm


class IndexView(TemplateView):
    """View for the index page"""
    template_name = 'keybar/web/index.html'


class RegisterView(CreateView):
    template_name = 'keybar/web/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('keybar-index')

    def form_valid(self, form):
        response = super(RegisterView, self).form_valid(form)
        messages.success(self.request, _('You registered successfully'))
        return response


class LoginView(FormView):
    template_name = 'keybar/web/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('keybar-index')

    def form_valid(self, form):
        response = super(LoginView, self).form_valid(form)
        messages.success(self.request, _('You were logged in successfully'))
        auth_login(self.request, form.get_user())
        return response
