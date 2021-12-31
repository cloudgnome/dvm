from functools import wraps
from urllib.parse import urlparse
from user.views import SignInView
from user.models import User

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url,redirect
REDIRECT_FIELD_NAME = 'next'


def user_passes_test(test_func, login_url=None,redirect_path='/',redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)

            return SignInView.as_view()(request, *args,**kwargs)
        return _wrapped_view
    return decorator

def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator