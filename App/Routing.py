from django.urls import path
# Consumers
from . import Consumer

websocket_urlpatterns = [
    path('ws/sc/<str:RoomName>/<str:UserName>/',
         Consumer.MySyncConsumer.as_asgi()),
    path('ws/ac/<str:RoomName>/<str:UserName>/',
         Consumer.MyAsyncConsumer.as_asgi()),
]
