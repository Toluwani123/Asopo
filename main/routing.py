from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'wss/creator_chat/(?P<booth_name>\w+)/$', consumers.BoothConsumer.as_asgi()),
]