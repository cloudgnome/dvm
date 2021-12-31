from django.shortcuts import render
from catalog.models import Offer,Auction
from django.http import Http404

def category(request,model,category_id):
    try:
        Model = eval(model)
    except:
        raise Http404()

    items = Model.objects.filter(category__id=category_id)

    return render(request,'%ss.html' % model.lower(),{'%ss' % model.lower():items})