from django.utils.translation import ugettext_lazy as _
import floppyforms.__future__ as forms

from keybar.models.user import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label=_('Username'),
        widget=forms.TextInput)
    password = forms.CharField(label=_('Password'),
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
