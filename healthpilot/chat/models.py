from django.db import models
from client.models import User


class PrivateChat(models.Model): #TODO make the id a uuid
    participants = models.ManyToManyField(User, related_name='private_chats')
    # There must have to be only two users so raise errors

    def __str__(self):
        return f'private Chat ID {self.id}'

class GroupChat(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False)
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='group_chats')
    total_user = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        self.total_user = self.participants.count()
        super(GroupChat, self).save(*args, **kwargs)

    def __str__(self):
        return f'Group -> {self.name}'

class Message(models.Model):
    priv_chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, related_name='private_messages', null=True, blank=True)
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='group_messages', null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"From: {self.sender}"

    class Meta:
        ordering = ('timestamp',)
#TODO i want to delay it since it have a lot of feature envluding status online, seen message, friends, cancel friend request, videos .....

# chatboot conversation

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class ChatbotMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    context = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)