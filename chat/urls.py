from django.urls import re_path
from user.decorators import login_required

from .views import *

urlpatterns = [
    re_path(r'^send/(?P<reciever_id>[0-9]+)$',login_required(send)),
    re_path(r'^messages$',login_required(messages)),
    re_path(r'^(?P<id>[0-9]+)$',login_required(chat)),
]