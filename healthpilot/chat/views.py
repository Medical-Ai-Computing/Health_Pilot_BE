from rest_framework.views import APIView
from rest_framework.response import Response
from channels.layers import get_channel_layer


from .models import PrivateChat, GroupChat, Message
from .serializers import PrivateChatSerializer, GroupChatSerializer, MessageSerializer

class PrivateChatView(APIView):
    def post(self, request):
        serializer = PrivateChatSerializer(data=request.data)
        if serializer.is_valid():
            private_chat = serializer.save()
            return Response(PrivateChatSerializer(private_chat).data)
        return Response(serializer.errors, status=400)

class GroupChatView(APIView):
    def post(self, request):
        serializer = GroupChatSerializer(data=request.data)
        if serializer.is_valid():
            group_chat = serializer.save()
            return Response(GroupChatSerializer(group_chat).data)
        return Response(serializer.errors, status=400)

class MessageView(APIView):
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save()
            channel_layer = get_channel_layer()
            if message.chat:
                chat_id = message.chat.id
            elif message.group_chat:
                chat_id = message.group_chat.id
            async_to_sync(channel_layer.group_send)(
                f'chat_{chat_id}',
                {'type': 'chat_message', 'message': MessageSerializer(message).data}
            )
            return Response(MessageSerializer(message).data)
        return Response(serializer.errors, status=400)
