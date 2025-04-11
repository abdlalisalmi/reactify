from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import reactify.routing

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(reactify.routing.websocket_urlpatterns)
        ),
    }
)
