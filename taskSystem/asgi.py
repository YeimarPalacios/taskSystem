
# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import myapp.notifications.routing
from myapp.security.middleware_websockets import CustomAuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskSystem.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
         CustomAuthMiddlewareStack(
            URLRouter(
                myapp.notifications.routing.websocket_urlpatterns
            )
        )
    ),
})
