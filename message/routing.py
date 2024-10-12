from django.urls import re_path


from .consumers import ChatConsumer

# application = ProtocolTypeRouter({
#     'wwbsocket': AllowedHostsOriginValidator(
#         AuthMiddlewareStack(

#         )
#     )
# })

websocket_urlpatterns = [
   re_path(r'ws/notifications/(?P<user_id>\d+)/$', ChatConsumer.as_asgi()),
    # path('wss/notifications/<str:room_name>/', ChatConsumer.as_asgi()),
]