from django.shortcuts import render
from catalog.models import Offer
from django.http import Http404

def offer(request,id):
    try:
        context = {
            'offer':Offer.objects.get(id=id),
        }
    except Offer.DoesNotExist:
        raise Http404()

    return render(request,'catalog/offer.html',context)