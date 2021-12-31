from django import forms
from django.utils.translation import ugettext_lazy as _
from user.models import User

class UserSocialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False

    class Meta:
        model = User
        fields = ('email','fname','social_id','social_type')

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label=_('New password'),widget=forms.PasswordInput(attrs={'placeholder': _('New password*')}))
    password2 = forms.CharField(label=_('Password again'),widget=forms.PasswordInput(attrs={'placeholder': _('Password again*')}))
    class Meta:
        fields = ('__all__',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords dont match"))
        return password2

class RecoverForm(forms.Form):
    email = forms.EmailField(label=_("your email"),required=True)

    class Meta:
        fields = ('email',)

class SignInForm(forms.Form):
    login = forms.CharField(label=_('Login*:'),widget=forms.TextInput(attrs={'placeholder': 'Login','title':'Login'}),required=True)
    password = forms.CharField(label=_('Password*:'),widget=forms.PasswordInput(attrs={'placeholder': _('Password'),'autocomplete':'password'}))

    class Meta:
        fields = "__all__"

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'),widget=forms.PasswordInput(attrs={'placeholder': _('Password*')}))
    password2 = forms.CharField(label=_('Password Again'),widget=forms.PasswordInput(attrs={'placeholder': _('Password Again*')}))
    email = forms.CharField(label=_('Email'),widget=forms.TextInput(attrs={'placeholder': _('Email')}))
    fname = forms.CharField(label=_('Fname'),widget=forms.TextInput(attrs={'placeholder': _('Fname')}))
    lname = forms.CharField(label=_('Lname'),widget=forms.TextInput(attrs={'placeholder': _('Lname')}))
    phone = forms.CharField(label=_('Phone'),widget=forms.TextInput(attrs={'placeholder': _('Phone')}))

    def save(self, *args, commit = True, **kwargs):
        user = super().save(*args, **kwargs)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords dont match"))
        return password2

    class Meta:
        fields = '__all__'
        model = User
        exclude = ('password','social_type','social_id','is_active','image','balance')