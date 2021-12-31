from django import forms
from catalog.models import Offer,Category
from django.utils.translation import ugettext_lazy as _
from catalog.widgets import *

class AddOfferForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'),widget=forms.TextInput(attrs={'placeholder': _('Name')}))
    description = forms.CharField(label=_('Description'),widget=forms.Textarea(attrs={'placeholder': _('Description')}))
    location_text = forms.CharField(label=_('Location'),widget=forms.TextInput(attrs={'placeholder': _('Enter first letters')}))
    price = forms.CharField(label=_('Price'),widget=forms.TextInput(attrs={'placeholder': _('Price')}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=CategoryWidget())

    class Meta:
        model = Offer
        fields = ('name','condition','price','category','description','location_text','location_lat','location_lng')
        exclude = ('status','sold','views')
        widgets = {'location_lat':forms.HiddenInput(),'location_lng':forms.HiddenInput()}

class EditOfferForm(AddOfferForm):
    class Meta:
        model = Offer
        fields = ('name','condition','price','category','description','location_text','location_lat','location_lng')
        exclude = ('status','sold','views')
        widgets = {'location_lat':forms.HiddenInput(),'location_lng':forms.HiddenInput()}