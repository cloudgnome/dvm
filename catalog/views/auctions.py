from django.shortcuts import render
from catalog.models import Auction

def auctions(request):
    context = {
        'auctions':Auction.objects.all(),
    }
    return render(request,'catalog/auctions.html',context)