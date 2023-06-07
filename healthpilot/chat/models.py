from django.db import models
from client.models import User

class PrivateChat(models.Model):
    participants = models.ManyToManyField(User, related_name='private_chats')

    def __str__(self):
        return 'private Chat ID {id}'

class GroupChat(models.Model):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='group_chats')
    total_user = models.IntegerField(default=1)

    # def save(self, *args, **kwargs):
    #     self.total_user = self.participants.count()
    #     super(GroupChat, self).save(*args, **kwargs)

    def __str__(self):
        return 'Group {name}'

class Message(models.Model):
    chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, related_name='private_messages', null=True)
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='group_messages', null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# chatboot conversation

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class ChatbotMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    context = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)