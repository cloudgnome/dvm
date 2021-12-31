from django.shortcuts import render
from catalog.models import Offer

def offers(request):
    context = {
        'offers':Offer.objects.all(),
    }
    return render(request,'catalog/offers.html',context)