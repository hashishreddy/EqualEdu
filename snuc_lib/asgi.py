# snuc_lib/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns  # Import WebSocket URL patterns from "chat" app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snuc_lib.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Include WebSocket URL patterns from "chat" app here
        )
    ),
})

