# your_project/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, include

from chat import routing as chat_routing  # Import the WebSocket routing from your chat app

application = ProtocolTypeRouter({
    "websocket": URLRouter(
        chat_routing.websocket_urlpatterns
    ),
})
