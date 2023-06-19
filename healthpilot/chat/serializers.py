from rest_framework import serializers
from .models import PrivateChat, GroupChat, Message, Conversation, ChatbotMessage

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender','content', 'id', 'priv_chat', 'group_chat']

class PrivateChatSerializer(serializers.ModelSerializer):
    private_messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = PrivateChat
        fields = ['id', 'participants', 'private_messages']

class GroupChatSerializer(serializers.ModelSerializer):
    group_messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = GroupChat
        fields = ['name', 'participants', 'group_messages']


# Chatbot serializer
class ChatbotMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotMessage
        fields = ('sender', 'context', 'timestamp', 'conversation')

class ConversationSerializer(serializers.ModelSerializer):
    messages = ChatbotMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('user', 'messages', 'timestamp')