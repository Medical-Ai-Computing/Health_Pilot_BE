from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Profile, UserActivation
import base64
from uuid import uuid4
from django.conf import settings
from .utils import send_activation_email, generate_token
from django.contrib.auth.hashers import make_password

class UserActivationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = UserActivation
        fields = ('user', 'activation_token')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        return token

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    activation_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'activation_token')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        
        activation_token = uuid4().hex
        
        user.is_active = False
        user.save()

        user_activation = UserActivation(user=user, activation_token=activation_token)
        user_activation.save()
        

        # Add the user to the "healthpilot" permission group
        group, created = Group.objects.get_or_create(name='healthpilot')
        user.groups.add(group)
        user.save()

        try:
            # send the activation email to the user
            send_activation_email(user.email, activation_token)
        except:
            return user

        return user


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']

class UserDetailSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    groups = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",
            "image_url"
        ]

    def get_id(self, obj):
        return obj.id

    def get_groups(self, obj):
        return [group.name for group in obj.groups.all()]

    def get_image_url(self, obj):
        try:
            profile = obj.profile
            image_url = str(profile.image)
            return settings.MEDIA_URL + image_url
        except:
            return None