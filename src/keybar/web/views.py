from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView

from keybar.core.mixins import LoginRequiredMixin
from keybar.web.forms import EntryForm


class IndexView(TemplateView):
    """View for the index page"""
    template_name = 'keybar/web/index.html'


class EntryFormView(LoginRequiredMixin, FormView):
    template_name = 'keybar/web/entry.html'
    form_class = EntryForm
    success_url = reverse_lazy('keybar-index')

    def form_valid(self, form):
        form.save(self.request)
        return HttpResponseRedirect(self.get_success_url())
