from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView, ListView

from keybar.core.mixins import LoginRequiredMixin
from keybar.models.entry import Entry
from keybar.web.forms import EntryForm


class IndexView(TemplateView):
    """View for the index page"""
    template_name = 'keybar/web/index.html'


class VaultView(ListView):
    template_name = 'keybar/web/entries.html'

    def get_queryset(self):
        return Entry.objects.filter(created_by=self.request.user)


class EntryFormView(LoginRequiredMixin, FormView):
    template_name = 'keybar/web/entry.html'
    form_class = EntryForm
    success_url = reverse_lazy('keybar-index')

    def form_valid(self, form):
        form.save(self.request)
        return HttpResponseRedirect(self.get_success_url())
