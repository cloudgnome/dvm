from user.models import User
from django.http import Http404,JsonResponse
from json import loads
from catalog.utils import is_ajax

def match(request,model):
    if is_ajax(request):
        Model = eval(model.title())
        try:
            Model.objects.get(**loads(request.body))
            return JsonResponse({'result':False})
        except Model.DoesNotExist:
            return JsonResponse({'result':True})
    else:
        raise Http404()