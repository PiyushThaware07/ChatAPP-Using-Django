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

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(App.Routing.websocket_urlpatterns),
})

# Vercel Doesn't know application varibale so use below it only knwos app
app = application
