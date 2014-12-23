import itertools

from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView, ListView, View, FormView)
from django.utils.translation import ugettext_lazy as _
from user_sessions.views import SessionMixin as UserSessionMixin

from keybar.core.mixins import LoginRequiredMixin
from keybar.models.entry import Entry
from keybar.web.forms import (
    EntryForm, UpdateEntryForm, ViewEntryForm, SetupTotpForm)
from keybar.utils.totp import generate_qr_code_response


class IndexView(TemplateView):
    """View for the index page"""
    template_name = 'keybar/web/index.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('keybar-vault'))
        return super(IndexView, self).get(*args, **kwargs)


class VaultView(ListView):
    template_name = 'keybar/web/vault.html'

    def get_queryset(self):
        return Entry.objects.filter(owner=self.request.user)


class TagsView(ListView):
    def get_queryset(self):
        qset = (Entry.objects
            .filter(owner=self.request.user)
            .values_list('tags', flat=True))
        return itertools.chain.from_iterable(qset)

    def render_to_response(self, context, **kwargs):
        return JsonResponse({'tags': list(context['object_list'])}, **kwargs)


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

    def get_form_kwargs(self):
        kwargs = super(EntryDetailFormView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        if 'unlock' in self.request.POST:
            return self.render_to_response(self.get_context_data(form=form))

        form.save(self.request)
        return HttpResponseRedirect(self.get_success_url())


class SetupTotpView(LoginRequiredMixin, FormView):
    template_name = 'keybar/web/setup-totp.html'
    form_class = SetupTotpForm
    success_url = reverse_lazy('keybar-vault')

    def get_form_kwargs(self):
        kwargs = super(SetupTotpView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        messages.success(self.request,
            _('Google Authenticator successfully verified'))
        return HttpResponseRedirect(self.get_success_url())


class TotpQrCodeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return generate_qr_code_response(request)


class SessionListView(LoginRequiredMixin, UserSessionMixin, ListView):
    template_name = 'account/session-list.html'

    def get_context_data(self, **kwargs):
        kwargs['session_key'] = self.request.session.session_key
        return super(SessionListView, self).get_context_data(**kwargs)


class SessionDeleteView(LoginRequiredMixin, UserSessionMixin, DeleteView):
    def get_success_url(self):
        return str(reverse_lazy('keybar-account-session-list'))
