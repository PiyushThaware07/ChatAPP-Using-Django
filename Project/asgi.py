"""
ASGI config for Project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
# Imports
from channels.routing import ProtocolTypeRouter, URLRouter
import App.Routing

# ASGIN Deploy
from some_asgi_library import AmazingMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')

application =  AmazingMiddleware(ProtocolTypeRouter({
    'https': get_asgi_application(),
    'websocket': URLRouter(App.Routing.websocket_urlpatterns),
})
)
