from django.utils import timezone
from datetime import datetime, timedelta
import requests
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from client.models import User, Membership

@receiver(post_save, sender=User)
def create_membership(sender, instance, *args, **kwargs):
    print('from signals-------------------------')
    member = Membership.objects.get_or_create(user=instance, membership_type='F')
    print(member, 'is created in membership table')
    