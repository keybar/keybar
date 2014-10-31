from django.utils.translation import ugettext_lazy as _
from django.contrib import auth
import floppyforms.__future__ as forms

from keybar.models.user import User


class RegisterForm(forms.ModelForm):
    name = forms.CharField(label=_('Your name'), widget=forms.TextInput)
    email = forms.EmailField(label=_('Email'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'email')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user



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
