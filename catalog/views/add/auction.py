from django.views.generic import View
from catalog.forms import AddAuctionForm
from django.shortcuts import render,redirect
from django.http import JsonResponse
from json import loads

class AddAuctionView(View):
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('/user/signin')

        context = {
            'form':AddAuctionForm()
        }

        return render(request,'catalog/add/auction.html',context)

    def post(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('/user/signin')

        form = AddAuctionForm(loads(request.body))
        if form.is_valid():
            auction = form.save(commit=False)
            auction.user = request.user
            auction.save()
            return JsonResponse({'result':True,'auctionId':auction.id})

        return JsonResponse({'result':False,'errors':form.errors})