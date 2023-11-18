from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                raise ValidationError({'detail': 'Incorrect password.'})
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(email=username)
                if user.check_password(password):
                    return user
                else:
                    raise ValidationError({'detail': 'Incorrect password.'})

            except UserModel.DoesNotExist:
                raise ValidationError({'detail': 'User not found.'})

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None