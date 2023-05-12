from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins, status, viewsets

import logging
from django.db.models import Count
from django.http import QueryDict
from django.utils import timesince, timezone
from .models import User, EmergencyContact, Disease, Article, Doctor, Payment, Membership
from .serializers import UserSerializer, DiseaseSerializer, ArticleSerializer,EmergencyContactSerializer, DoctorsSerializer, PaymentSerializer

class UserAPIView(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class ArticleAPIView(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

class EmergencyContactAPIView(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    serializer_class = EmergencyContactSerializer
    queryset = EmergencyContact.objects.all()

class DiseaseViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    serializer_class = DiseaseSerializer
    queryset = Disease.objects.all()


class DoctorViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    ''' api view method for doctors
    1. Create Doctors
    2. List doctors
    3. Retrive doctors
    4. Update
    5. Remove Doctors'''

    serializer_class = DoctorsSerializer
    queryset = Doctor.objects.all()

class PaymentCreateView(generics.CreateAPIView):
    '''used to process the payment'''
    # permission_classes = [IsAuthenticated] # authenticated users can have editable forms
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        print('before request data', request.data['user'], request.data)
        # membership_type = request.user.membership.membership_type
        membership_type = User.objects.get(id=request.data['user']).membership

        if membership_type == 'F':
            # request.user.membership.membership_type = 'premium'
            # request.user.membership.save()
            print('---------- membership type is Free----------')

            user_id = request.data['user']
            print(user_id, 'user--id--id')
            membership = Membership() # user.membership
            membership.activate_premium_membership()
        else:
            message = 'This user is already Premium user'
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, *args, **kwargs)
        #TODO try to add 400 bad request up here if the payment not successfull

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        serializer.instance.is_paid = True
        serializer.instance.save()
        return Response(serializer.data, status=HTTP_201_CREATED)