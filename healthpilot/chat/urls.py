from django.urls import path
from .views import PrivateChatView, GroupChatView, MessageView
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:chat_id>/', ChatConsumer.as_asgi()),
]

urlpatterns = [
    path('private-chat/', PrivateChatView.as_view(), name='private_chat'),
    path('group-chat/', GroupChatView.as_view(), name='group_chat'),
    path('message/', MessageView.as_view(), name='message'),
]

