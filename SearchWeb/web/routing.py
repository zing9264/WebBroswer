from django.urls import re_path
from web import consumers

websocket_urlpatterns = [
  re_path('ws/chat/', consumers.Consumer),
]