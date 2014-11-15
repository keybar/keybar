from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.utils.translation import ugettext_lazy as _
from allauth.account.signals import user_signed_up


from keybar.core.mixins import LoginRequiredMixin
from keybar.models.entry import Entry
from keybar.web.forms import EntryForm, UpdateEntryForm, ViewEntryForm


class IndexView(TemplateView):
    """View for the index page"""
    template_name = 'keybar/web/index.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('keybar-vault'))
        return super(IndexView, self).get(*args, **kwargs)


class VaultView(ListView):
    template_name = 'keybar/web/entries.html'

    def get_queryset(self):
        return Entry.objects.filter(created_by=self.request.user)


class EntryAddFormView(LoginRequiredMixin, CreateView):
    template_name = 'keybar/web/entry-update.html'
    form_class = EntryForm
    model = Entry
    success_url = reverse_lazy('keybar-vault')

    def form_valid(self, form):
        self.object = form.save(self.request)
        return HttpResponseRedirect(self.get_success_url())


class EntryUpdateFormView(LoginRequiredMixin, UpdateView):
    template_name = 'keybar/web/entry-update.html'
    form_class = UpdateEntryForm
    model = Entry
    success_url = reverse_lazy('keybar-vault')

    def form_valid(self, form):
        form.save(self.request)
        messages.success(self.request, _('Entry updated successfully'))
        return HttpResponseRedirect(self.get_success_url())


class EntryDetailFormView(LoginRequiredMixin, UpdateView):
    template_name = 'keybar/web/entry-detail.html'
    form_class = ViewEntryForm
    model = Entry
    success_url = reverse_lazy('keybar-vault')

    def get_template_names(self):
        if 'unlock' in self.request.POST:
            return ['keybar/web/entry-detail.html']
        return super(EntryDetailFormView, self).get_template_names()

    def get_form_kwargs(self):
        kwargs = super(EntryDetailFormView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        if 'unlock' in self.request.POST:
            return self.render_to_response(self.get_context_data(form=form))

        form.save(self.request)
        return HttpResponseRedirect(self.get_success_url())
