from .models import Profile, UserActivation
from rest_framework import generics
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import (
    RegisterSerializer,
    UserDetailSerializer,
    ProfilePictureSerializer,
    MyTokenObtainPairSerializer,
    UserActivationSerializer,
)

from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
)


from rest_framework.permissions import (
    AllowAny,
    # IsOwner,
)
from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.generics import (
    UpdateAPIView,
)
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework import status

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password


from .utils import send_activation_email, generate_token


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class UpdateProfilePictureAPIView(UpdateAPIView):
    queryset = Profile.objects.all()
    lookup_field = "id"
    serializer_class = ProfilePictureSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        profile_picture = self.request.FILES.get('profile_picture')
        if profile_picture:
            self.get_object().profile_picture = profile_picture
            self.get_object().save()
        return super().update(request, *args, **kwargs)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class DetailUserAPIView(RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the details of a user instance. Searches user using id field.

    put:
        Updates an existing user. Returns updated user data

        parameters: [id, title, body, description, image]

    delete:
        Delete an existing user

        parameters = [id]
    """

    queryset = User.objects.all()
    lookup_field = "id"
    serializer_class = UserDetailSerializer
    permission_classes = [AllowAny] #[IsOwner]


class UserActivationAPIView(APIView):
    queryset = UserActivation.objects.all()
    serializer_class = UserActivationSerializer
    permission_classes = [AllowAny]

    def get(self, request, activation_token, *args, **kwargs):
        try:
            user_activation = self.queryset.get(activation_token=activation_token)
            user = user_activation.user
        except UserActivation.DoesNotExist:
            return Response({'message': 'Activation link is invalid or has already been used.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = True
        user.save()
        user_activation.delete()
        
        return Response({'message': 'User activation successful. You can now log in to the system.'})


class ResendActivationCodeAPIView(APIView):
    queryset = UserActivation.objects.all()
    serializer_class = UserActivationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        if email is None:
            return Response({'message': 'Email address is required to resend activation code.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with provided email address does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({'message': 'User is already activated. No need to resend activation code.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_activation = self.queryset.get(user=user)
        except UserActivation.DoesNotExist:
            return Response({'message': 'Activation code not found for provided email address.'}, status=status.HTTP_400_BAD_REQUEST)

        activation_token = user_activation.activation_token
        # send the activation token to the user's email address
        # ...

        try:
            # send the activation email to the user
            send_activation_email(user.email, activation_token)
        except:
            return Response({'message': 'We can\'t send the activation code now. Please try latter.'}, status=status.HTTP_500_BAD_REQUEST)
            # return user

        return Response({'message': 'Activation code resent successfully to the provided email address.'})