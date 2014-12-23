import datetime
import time

import floppyforms.__future__ as forms
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from cryptography.fernet import InvalidToken as InvalidFernetToken
from cryptography.hazmat.primitives.twofactor.totp import InvalidToken as InvalidTotpToken

from keybar.models.user import User
from keybar.models.entry import Entry
from keybar.widgets import Select2Widget
from keybar.utils.totp import verify_totp_code


class RegisterForm(forms.ModelForm):
    name = forms.CharField(label=_('Your name'),
        widget=forms.TextInput(
            attrs={'placeholder': _('e.g Jorah Mormont')}))
    email = forms.EmailField(label=_('Email'))

    class Meta:
        model = User
        fields = ('name', 'email')

    def signup(self, request, user):
        user.name = self.instance.name
        user.email = self.instance.email
        user.save()


class SetupTotpForm(forms.Form):
    totp_code = forms.CharField(label=_('TOTP Code'),
        help_text=_('Please open your Google Authenticator App and enter the code.'))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(SetupTotpForm, self).__init__(*args, **kwargs)

    def clean_totp_code(self):
        try:
            verify_totp_code(self.request.user, self.data['totp_code'])
        except InvalidTotpToken:
            dt = datetime.datetime.fromtimestamp(time.time())
            raise ValidationError(
                'Invalid TOTP code! Make sure your time is correct: {0}'.format(
                    dt))


class EntryForm(forms.ModelForm):
    value = forms.CharField(label=_('Secure value to store'),
        widget=forms.PasswordInput())
    password = forms.CharField(label=_('Password to unlock this entry.'),
        widget=forms.PasswordInput())
    force_two_factor_authorization = forms.BooleanField(
        label=_('Force Two-Factor Authentication'), required=False)

    class Meta:
        model = Entry
        fields = (
            'title', 'url', 'identifier', 'value', 'tags', 'description',
            'force_two_factor_authorization')
        widgets = {
            'title': forms.TextInput(),
            'identifier': forms.TextInput(),
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': Select2Widget()
        }

    def save(self, request, commit=True):
        self.instance.owner = request.user

        if self.cleaned_data['value']:
            self.instance.set_value(
                self.cleaned_data['password'],
                self.cleaned_data['value'])

        return super(EntryForm, self).save(commit=commit)


class UpdateEntryForm(EntryForm):
    value = forms.CharField(label=_('Secure value to store'),
        widget=forms.PasswordInput(), required=False)
    password = forms.CharField(label=_('Password to unlock and update this entry.'),
        widget=forms.PasswordInput())


class ViewEntryForm(EntryForm):
    value = forms.CharField(label=_('Decrypted value'))
    totp_code = forms.CharField(label=_('TOTP Secret'),
        help_text=_('Please open your Google Authenticator App and enter the code.'))

    class Meta(EntryForm.Meta):
        fields = (
            'title', 'tags', 'description', 'identifier', 'value')

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ViewEntryForm, self).__init__(*args, **kwargs)

        if 'unlock' not in self.request.POST:
            del self.fields['value']

        del self.fields['force_two_factor_authorization']

    def clean_password(self):
        if 'unlock' in self.request.POST:
            try:
                data = self.data.copy()
                data['value'] = self.instance.decrypt(self.request.POST['password'])
                self.data = data
            except InvalidFernetToken:
                del self.fields['value']
                raise ValidationError('Invalid password!')

    def clean_totp_code(self):
        try:
            if self.instance.force_two_factor_authorization:
                verify_totp_code(self.request.user, self.data['totp_code'])
        except InvalidTotpToken:
            raise ValidationError('Invalid TOTP code!')

    def clean(self):
        cleaned_data = super(ViewEntryForm, self).clean()
        self.errors.pop('value', None)

        if not self.errors:
            del self.fields['password']
            del self.fields['totp_code']

        return cleaned_data
