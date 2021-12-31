from django.shortcuts import render,redirect
from user.models import User
from django.views.generic import View
from django.http import JsonResponse

class EditView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_anonymous:
            return redirect('/user/signin/')

        try:
            request.user.country = Country.objects.get(id=request.user.country_id).name.replace('ru=','')
        except:
            pass
        try:
            request.user.city = City.objects.get(id=request.user.city_id).name.replace('ru=','')
        except:
            pass

        return render(request,'user/edit.html',{'view':'EditView'})

    def post(self,request,*args,**kwargs):
        form = EditForm(loads(request.body))
        if form.is_valid():
            extended = loads(request.user.extended)
            extended['profile'].update(form.cleaned_data)
            request.user.birthday = form.cleaned_data['birthday']
            request.user.country_id = form.cleaned_data['country_id']
            request.user.city_id = form.cleaned_data['city_id']
            request.user.extended = dumps(extended)
            request.user.save()
            return JsonResponse({'result':True})

        return JsonResponse({'result':False,'errors':form.errors})