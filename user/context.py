from user.models import AnonymousUser
from system.settings import JS_BUILD,CSS_BUILD

def auth(request):
    """
    Return context variables required by apps that use Django's authentication
    system.
    If there is no 'user' attribute in the request, use AnonymousUser (from
    django.contrib.auth).
    """
    if hasattr(request, 'user'):
        user = request.user
    else:
        user = AnonymousUser()

    context = {
        'user': user,
        'request':request,
        # 'perms': PermWrapper(user),
    }
    if not request.is_ajax():
        context['JS_BUILD'] = JS_BUILD
        context['CSS_BUILD'] = CSS_BUILD

    return context