# LicensePlateRecognition/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from anpr_project.anpr_app.detection import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anpr_project.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
