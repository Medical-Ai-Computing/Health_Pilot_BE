from django.conf.urls import include
from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .views import *

router = DefaultRouter()
router.register('users', UserAPIView, basename='users')

# users_router = NestedDefaultRouter(router, 'client', lookup='client')
# users_router.register('users', UserAPIView, basename='client-users')

urlpatterns = [
    path('', include(router.urls)),
    # path('', include(users_router.urls)),
]