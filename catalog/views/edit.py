from django.views.generic import View
from catalog.forms import EditAuctionForm,EditOfferForm
from catalog.models import Auction,Offer
from django.shortcuts import render
from django.http import Http404,JsonResponse
from json import loads

class EditView(View):
    def get(self,request,*args,**kwargs):
        try:
            Model = eval("%s" % kwargs.get('model'))
        except:
            raise Http404()

        try:
            obj = Model.objects.get(id=kwargs.get('id'),user=request.user)
        except Model.DoesNotExist:
            raise Http404()

        form = eval("Edit%sForm" % kwargs.get('model'))(instance=obj)

        return render(request,'edit/%s.html' % kwargs.get('model').lower(),{'obj':obj,'form':form})

    def post(self,request,*args,**kwargs):
        try:
            Model = eval("%s" % kwargs.get('model'))
        except:
            raise Http404()

        try:
            obj = Model.objects.get(id=kwargs.get('id'),user=request.user)
        except Model.DoesNotExist:
            raise Http404()

        form = eval("Edit%sForm" % kwargs.get('model'))(loads(request.body),instance=obj)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({'result':True,'objectId':obj.id})
        else:
            return JsonResponse({'result':False,'errors':form.errors})