from django.views.generic import View
from catalog.forms import AddOfferForm
from django.shortcuts import render,redirect
from django.http import JsonResponse
from json import loads

class AddOfferView(View):
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('/user/signin')

        context = {
            'form':AddOfferForm()
        }

        return render(request,'catalog/add/offer.html',context)

    def post(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('/user/signin')

        form = AddOfferForm(loads(request.body))
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            offer.save()
            return JsonResponse({'result':True,'offerId':offer.id})

        return JsonResponse({'result':False,'errors':form.errors})