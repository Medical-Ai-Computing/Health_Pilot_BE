from django.contrib import admin
from .models import PrivateChat, GroupChat, Message, ChatbotMessage, Conversation

@admin.register(PrivateChat)
class PrivateChatAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PrivateChat._meta.fields]


@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GroupChat._meta.fields]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Message._meta.fields]

@admin.register(ChatbotMessage)
class ChatbotMessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ChatbotMessage._meta.fields]

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Conversation._meta.fields]
