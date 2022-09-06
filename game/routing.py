from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('game_socket/', consumers.GameSessionConsumer.as_asgi())
]