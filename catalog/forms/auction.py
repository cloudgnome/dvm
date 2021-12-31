from django import forms
from catalog.models import Auction,Category
from django.utils.translation import ugettext_lazy as _
from catalog.widgets import *

class AddAuctionForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'),widget=forms.TextInput(attrs={'placeholder': _('Name')}))
    description = forms.CharField(label=_('Description'),widget=forms.Textarea(attrs={'placeholder': _('Description')}))
    location_text = forms.CharField(label=_('Location'),widget=forms.TextInput(attrs={'placeholder': _('Enter first letters')}))
    start_price = forms.IntegerField(label=_('Start Price'),widget=forms.NumberInput(attrs={'placeholder': _('Start Price')}))
    buyout = forms.IntegerField(label=_('Buyout Price'),widget=forms.NumberInput(attrs={'placeholder': _('Buyout Price')}))
    bid_step = forms.IntegerField(label=_('Bid Step'),widget=forms.NumberInput(attrs={'placeholder': _('Bid Step')}))
    end_date = forms.CharField(widget=forms.DateInput(attrs={'type':'date','placeholder':_('Choose end date')}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=CategoryWidget())

    class Meta:
        model = Auction
        fields = ('name','condition','start_price','buyout','bid_step','category','end_date','description','location_text','location_lat','location_lng')
        exclude = ('status','sold','views')
        widgets = {'location_lat':forms.HiddenInput(),'location_lng':forms.HiddenInput()}

class EditAuctionForm(AddAuctionForm):
    class Meta:
        model = Auction
        fields = ('name','condition','start_price','buyout','bid_step','category','end_date','description','location_text','location_lat','location_lng')
        exclude = ('status','sold','views')
        widgets = {'location_lat':forms.HiddenInput(),'location_lng':forms.HiddenInput()}