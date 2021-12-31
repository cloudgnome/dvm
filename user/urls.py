from django.urls import re_path
from user.views import *
from user.decorators import login_required

urlpatterns = [
    re_path(r'^signout$', login_required(signout)),
    re_path(r'^signup$', SignUpView.as_view()),
    re_path(r'^signin$', SignInView.as_view()),
    re_path(r'^edit$', login_required(EditView.as_view())),
    re_path(r'^recover$',recover),
    re_path(r'^change-password$',ChangePasswordView.as_view()),
    re_path(r'^activate$',activate),
    re_path(r'^profile$',login_required(main)),
    re_path(r'^business$',login_required(business)),
    re_path(r'^interface$',login_required(interface)),
    re_path(r'^payments$',login_required(payments)),
    re_path(r'^settings$',login_required(settings)),
    re_path(r'^view$',login_required(view)),
    re_path(r'^add/image',login_required(image))
]