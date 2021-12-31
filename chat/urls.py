from django.conf.urls import url
from user.decorators import login_required

from .views import *

urlpatterns = [
    url(r'^send/(?P<reciever_id>[0-9]+)$',login_required(send)),
    url(r'^messages$',login_required(messages)),
    url(r'^(?P<id>[0-9]+)$',login_required(chat)),
]