from django.urls import path
from auth.views import MyObtainTokenPairView, RegisterView, DetailUserAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UpdateProfilePictureAPIView, UserActivationAPIView, ResendActivationCodeAPIView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('user/<int:id>/', DetailUserAPIView.as_view(), name='user_profile'),
    path('user/profile_picture/<int:id>/', UpdateProfilePictureAPIView.as_view(), name='user_picture_update'),
    path('activate/<str:activation_token>/', UserActivationAPIView.as_view(), name='activate'),
    path('resend-activation-code/', ResendActivationCodeAPIView.as_view(), name='resend-activation-code'),
]