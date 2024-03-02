from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('chat/message/', consumers.ChatConsumer.as_asgi()),
]