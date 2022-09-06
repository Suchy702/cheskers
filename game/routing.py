from django.urls import re_path 
from . import consumers

websocket_urlpatterns = [
    path('game_socket/', consumers.GameSessionConsumer.as_asgi())
]