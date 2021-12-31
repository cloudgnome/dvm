from django import forms
from django.utils.translation import gettext_lazy as _
from user.models import Business
from form_utils.forms import BetterModelForm

class BusinessForm(BetterModelForm):
    email = forms.CharField(label=_('Email'),widget=forms.EmailInput(attrs={'placeholder': _('Email')}))
    name = forms.CharField(label=_('Name'),widget=forms.TextInput(attrs={'placeholder': _('Name')}))
    phone = forms.CharField(label=_('Phone'),widget=forms.TextInput(attrs={'placeholder': _('Phone')}))
    country = forms.CharField(label=_('Country'),widget=forms.TextInput(attrs={'placeholder': _('Country')}))
    postal_code = forms.CharField(label=_('Postal Code'),widget=forms.TextInput(attrs={'placeholder': _('Postal Code')}))
    address = forms.CharField(label=_('Address'),widget=forms.TextInput(attrs={'placeholder': _('Address')}))
    website = forms.CharField(label=_('Web-site'),widget=forms.TextInput(attrs={'placeholder': _('Web-site')}))

    class Meta:
        fields = '__all__'
        model = Business
        exclude = ('user',)
        fieldsets = [
                    ('', {'fields':['name'],'legend':''}),
                    ('', {'fields':['email','phone'],'legend':''}),
                    ('', {'fields':['country','postal_code'],'legend':''}),
                    ('', {'fields':['address'],'legend':''}),
                    ('', {'fields':['website'],'legend':''}),
                ]