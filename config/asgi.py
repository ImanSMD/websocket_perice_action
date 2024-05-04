"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
from channels.routing import ProtocolTypeRouter ,URLRouter
from email.mime import application
from django.urls import path
import os
from typing import Protocol

from django.core.asgi import get_asgi_application

from PriceAction.consumers import PriceConsumer

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket' : URLRouter(
        [
            path('prices', PriceConsumer.as_asgi() )
        ]
    )
})
