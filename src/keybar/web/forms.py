from django.utils.translation import ugettext_lazy as _
from django.contrib import auth
import floppyforms.__future__ as forms

from keybar.models.user import User


class RegisterForm(forms.ModelForm):
    name = forms.CharField(label=_('Your name'),
        widget=forms.TextInput(
            attrs={'placeholder': _('e.g Jorah Mormont')}))
    email = forms.EmailField(label=_('Email'))

    class Meta:
        model = User
        fields = ('name', 'email')


class LoginForm(forms.Form):
    email = forms.EmailField(label=_('Email'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _('Please enter a correct email and password. '
                           'Note that both fields may be case-sensitive.'),
    }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.authenticated_user = None

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.authenticated_user = auth.authenticate(email=email, password=password)

            if self.authenticated_user is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login')

        return self.cleaned_data

    def get_user(self):
        return self.authenticated_user
