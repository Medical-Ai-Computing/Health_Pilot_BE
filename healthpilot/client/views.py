from django.shortcuts import render
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics, mixins, status, viewsets

import logging
from django.db.models import Count
from django.http import QueryDict
from django.utils import timesince, timezone
from .models import User
from .serializers import UserSerializer

class UserAPIView(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

