from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from keybar.web.forms import RegisterForm


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
