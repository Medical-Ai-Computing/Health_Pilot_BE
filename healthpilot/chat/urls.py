from django.urls import path, include
from rest_framework_nested import routers
from .views import PrivateChatView, GroupChatView, MessageView, ConversationViewSet, ChatbotMessageViewSet
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:chat_id>/', ChatConsumer.as_asgi()),
]

router = routers.DefaultRouter()
router.register('conversations', ConversationViewSet)

conversation_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register('chatbotmessages', ChatbotMessageViewSet, basename='conversation_messages')



urlpatterns = [
    path('private_chat/', PrivateChatView.as_view(), name='private_chat'),
    path('group_chat/', GroupChatView.as_view(), name='group_chat'),
    path('message/', MessageView.as_view(), name='message'),
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
    # path('start_conversation/', StartConversationView.as_view(), name='start-conversation'),
    # path('send_message/', SendMessageView.as_view(), name='send-message'),
    # path('clear_conversation/', ClearConversationView.as_view(), name='clear-conversation'),
]

