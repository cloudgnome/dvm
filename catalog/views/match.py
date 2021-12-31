from user.models import User
from django.http import Http404,JsonResponse
from json import loads

def match(request,model):
    if request.is_ajax():
        Model = eval(model.title())
        try:
            Model.objects.get(**loads(request.body))
            return JsonResponse({'result':False})
        except Model.DoesNotExist:
            return JsonResponse({'result':True})
    else:
        raise Http404()