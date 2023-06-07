from rest_framework import serializers
from .models import PrivateChat, GroupChat, Message, Conversation, ChatbotMessage

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class PrivateChatSerializer(serializers.ModelSerializer):
    private_messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = PrivateChat
        fields = '__all__'

class GroupChatSerializer(serializers.ModelSerializer):
    group_messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = GroupChat
        fields = ['name', 'participants']


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