#
#
#import os
#
#from django.core.asgi import get_asgi_application
#
#from channels.auth import AuthMiddlewareStack
#from channels.routing import ProtocolTypeRouter, URLRouter
#
#import PersonalArea.routing
#
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'volunteer.settings')
#
#django_asgi_app = get_asgi_application()
#application = ProtocolTypeRouter({
#    "http": django_asgi_app,
#    "websocket": AuthMiddlewareStack(
#        URLRouter(
#            PersonalArea.routing.websocket_urlpatterns
#        )
#    )
#})
import os

import django
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Quiz.settings')
django.setup()
from PersonalArea.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})