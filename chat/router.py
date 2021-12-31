from django.conf.urls import url

from .consumers.user import ChatConsumer

websocket_urlpatterns = [
    url(r'^chat$', ChatConsumer)
]