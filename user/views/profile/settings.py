from django.shortcuts import render
from user.forms import SettingsForm
from json import loads
from django.http import JsonResponse
from user.models import User
from catalog.base64_loader import load_image

def settings(request):
    if request.POST:
        form = SettingsForm(request.POST,instance=request.user)
        if form.is_valid():
            user = form.save()

        context = {'form':form}
    else:
        context = {
            'form':SettingsForm(instance=request.user)
        }
    return render(request,'user/profile/settings.html',context)

def image(request):
    try:
        request.user.image.delete(save=True)
        request.user.image = User.thumbnail(load_image(loads(request.body).get('image')))
        request.user.save()
        return JsonResponse({'result':True})
    except Exception as e:
        return JsonResponse({'result':False,'error':str(e)})
