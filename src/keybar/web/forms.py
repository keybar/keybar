from django.utils.translation import ugettext_lazy as _
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
