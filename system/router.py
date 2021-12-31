import os,sys
sys.path.append('/home/dd/dvm-market.com/')
sys.path.append('/usr/local/lib/python3.6/site-packages')

os.environ.setdefault("ASGI_APPLICATION", "system.router:application")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.settings")
import django
django.setup()

from chat.middleware import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.router

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.router.websocket_urlpatterns
        )
    ),
})