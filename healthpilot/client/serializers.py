from django.db.models import Q
from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    '''Used to get and update users'''
    class Meta:
        model = User
        fields = ['id','nick_name', 'full_name', 'date_of_birth', 'age', 'joined_at', 'gender']
        read_only_fields = ['id']