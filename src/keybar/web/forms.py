import floppyforms.__future__ as forms
from django.utils.translation import ugettext_lazy as _

from keybar.models.user import User
from keybar.models.entry import Entry


class RegisterForm(forms.ModelForm):
    name = forms.CharField(label=_('Your name'),
        widget=forms.TextInput(
            attrs={'placeholder': _('e.g Jorah Mormont')}))
    email = forms.EmailField(label=_('Email'))

    class Meta:
        model = User
        fields = ('name', 'email')

    def signup(self, request, user):
        import ipdb; ipdb.set_trace()
        pass


class EntryForm(forms.ModelForm):
    value = forms.CharField(label=_('Secure value to store'),
        widget=forms.PasswordInput())
    password = forms.CharField(label=_('Password to unlock this entry.'),
        widget=forms.PasswordInput())

    class Meta:
        model = Entry
        fields = ('title', 'description', 'identifier')
        widgets = {
            'title': forms.TextInput(),
            'identifier': forms.TextInput()
        }

    def save(self, request, commit=True):
        self.instance.created_by = request.user
        self.instance.set_value(
            self.cleaned_data['password'],
            self.cleaned_data['value'])

        return super(EntryForm, self).save(commit=commit)
