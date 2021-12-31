from django.shortcuts import redirect
from user.models import AnonymousUser
from django.contrib.auth.signals import user_logged_out
from django.http import JsonResponse

def signout(request):
    user = getattr(request, 'user', None)
    if hasattr(user, 'is_authenticated') and not user.is_authenticated:
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)

    if hasattr(request, 'user'):
        request.user = AnonymousUser()

    request.session.flush()

    if request.is_ajax():
        return JsonResponse({'result':1})
    else:
        return redirect('/')