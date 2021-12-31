from django.shortcuts import render
from catalog.models import Auction
from django.http import Http404

def auction(request,id):
    try:
        context = {
            'auction':Auction.objects.get(id=id),
        }
    except Auction.DoesNotExist:
        raise Http404()

    return render(request,'catalog/auction.html',context)