import floppyforms.__future__ as forms
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from cryptography.fernet import InvalidToken as InvalidFernetToken

from keybar.models.user import User
from keybar.models.entry import Entry
from keybar.widgets import Select2Widget


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


class EntryForm(forms.ModelForm):
    value = forms.CharField(label=_('Secure value to store'),
        widget=forms.PasswordInput())
    password = forms.CharField(label=_('Password to unlock this entry.'),
        widget=forms.PasswordInput())

    class Meta:
        model = Entry
        fields = ('title', 'url', 'identifier', 'value', 'tags', 'description')
        widgets = {
            'title': forms.TextInput(),
            'identifier': forms.TextInput(),
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': Select2Widget()
        }

    def save(self, request, commit=True):
        self.instance.owner = request.user
        self.instance.set_value(
            self.cleaned_data['password'],
            self.cleaned_data['value'])

        return super(EntryForm, self).save(commit=commit)


class UpdateEntryForm(EntryForm):
    pass


class ViewEntryForm(EntryForm):
    value = forms.CharField(label=_('Decrypted value'))

    class Meta(EntryForm.Meta):
        fields = ('title', 'tags', 'description', 'identifier', 'value')

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ViewEntryForm, self).__init__(*args, **kwargs)
        if 'unlock' not in self.request.POST:
            del self.fields['value']

    def clean_password(self):
        if 'unlock' in self.request.POST:
            try:
                data = self.data.copy()
                data['value'] = self.instance.decrypt(self.request.POST['password'])
                self.data = data
                del self.fields['password']
            except InvalidFernetToken:
                del self.fields['value']
                raise ValidationError('Invalid password!')

    def clean(self):
        cleaned_data = super(ViewEntryForm, self).clean()
        self.errors.pop('value', None)
        return cleaned_data
