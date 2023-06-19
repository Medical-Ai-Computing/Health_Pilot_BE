from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from asgiref.sync import async_to_sync

from .openai_chat import get_completion_from_messages

from client.models import User, UserProfile
from .models import PrivateChat, GroupChat, Message, Conversation, ChatbotMessage
from .serializers import PrivateChatSerializer, GroupChatSerializer, MessageSerializer, \
                         ConversationSerializer, ChatbotMessageSerializer

class PrivateChatView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        private_chats = PrivateChat.objects.all()
        serializer = PrivateChatSerializer(private_chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PrivateChatSerializer(data=request.data)
        if serializer.is_valid():
            private_chat = serializer.save()
            return Response(PrivateChatSerializer(private_chat).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupChatView(APIView):

    def get(self, request):
        private_chats = PrivateChat.objects.all()
        serializer = PrivateChatSerializer(private_chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GroupChatSerializer(data=request.data)
        if serializer.is_valid():
            group_chat = serializer.save()
            return Response(GroupChatSerializer(group_chat).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageView(APIView):

    def get(self, request):
        message = Message.objects.all()
        serializer = MessageSerializer(message, many=True)
        message.seen = True
        message.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save()
            channel_layer = get_channel_layer()

            if message.priv_chat:
                print('privateeeeeeeeeeeeeeeeeeeeee')
                chat_id = message.priv_chat.id
            elif message.group_chat:
                print('Groupppppppppppppppppppppppppp')
                chat_id = message.group_chat.id

            async_to_sync(channel_layer.group_send)(
                f'chat_{chat_id}',
                {'type': 'chat_message', 'message': MessageSerializer(message).data}
            )
            print(MessageSerializer(message).data)
            return Response(MessageSerializer(message).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Chatbot Conversation

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class ChatbotMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatbotMessage.objects.all()
    serializer_class = ChatbotMessageSerializer
    
    # @action(detail=False, methods=['post'])
    def create(self, request, *args, **kwargs):
        # try:
        #     self.user = User.objects.get(id=kwargs['pk'], 
        #                                  deleted_at=None)
        # except User.DoesNotExist:
        #     return Response("User Does Not Exist.", 
        #                     status=status.HTTP_400_BAD_REQUEST)
        print(request.data['context'], '***********************')
        user_input = request.data['context']
        response = get_completion_from_messages(user_input)
        print(response)

        return Response({'input': user_input, 'message': response})