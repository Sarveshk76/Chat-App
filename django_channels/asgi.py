"""
ASGI config for django_channels project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.sessions import SessionMiddlewareStack
from channels.auth import AuthMiddlewareStack
from django.urls import path
from main.consumers import ChatRoomConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_channels.settings')

django_asgi_app = get_asgi_application()

ws_patterns = [
    path('ws/home/<int:id>', ChatRoomConsumer.as_asgi()),
    # path('ws/home/chat/<room_name>/', ChatRoomConsumer.as_asgi())
]

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(URLRouter(ws_patterns))
    # Just HTTP for now. (We can add other protocols later.)
})