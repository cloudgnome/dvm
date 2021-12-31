from django.conf.urls import url
from user.views import *
from user.decorators import login_required

urlpatterns = [
    url(r'^signout$', login_required(signout)),
    url(r'^signup$', SignUpView.as_view()),
    url(r'^signin$', SignInView.as_view()),
    url(r'^edit$', login_required(EditView.as_view())),
    url(r'^recover$',recover),
    url(r'^change-password$',ChangePasswordView.as_view()),
    url(r'^activate$',activate),
    url(r'^profile$',login_required(main)),
    url(r'^business$',login_required(business)),
    url(r'^interface$',login_required(interface)),
    url(r'^payments$',login_required(payments)),
    url(r'^settings$',login_required(settings)),
    url(r'^view$',login_required(view)),
    url(r'^add/image',login_required(image))
]