from django import forms
from django.utils.translation import gettext_lazy as _

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label=_('Новый пароль'),widget=forms.PasswordInput(attrs={'placeholder': _('Новый пароль*')}))
    password2 = forms.CharField(label=_('Еще раз'),widget=forms.PasswordInput(attrs={'placeholder': _('Еще раз*')}))
    class Meta:
        fields = ('__all__',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Пароли не совпадают"))
        return password2

class ForgetPassForm(forms.Form):
    phone = forms.CharField(label=_("напомните свой номер телефона"),required=True)

    class Meta:
        fields = ('phone',)

class SignInForm(forms.Form):
    login = forms.CharField(max_length=16,label=_('Логин*:'),widget=forms.TextInput(attrs={'placeholder': 'Логин','title':'Логин'}),required=True)
    password = forms.CharField(label=_('Пароль*:'),widget=forms.PasswordInput(attrs={'placeholder': _('Пароль'),'autocomplete':'password'}))

    class Meta:
        fields = "__all__"

class SignUpForm(forms.Form):
    password1 = forms.CharField()
    password2 = forms.CharField()
    email = forms.EmailField()