from django.contrib import admin
from .models import PrivateChat, GroupChat, Message

@admin.register(PrivateChat)
class PrivateChatAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PrivateChat._meta.fields]


@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GroupChat._meta.fields]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Message._meta.fields]