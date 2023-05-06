from django.conf.urls import include
from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .views import *

router = DefaultRouter()
router.register('users', UserAPIView, basename='users')
router.register('emergency_contact', UserAPIView, basename='emergency')
router.register('disease', UserAPIView, basename='disease')
router.register('article', UserAPIView, basename='articles')


emergency_contact_router = NestedDefaultRouter(router, 'emergency_contact', lookup='user')
emergency_contact_router.register('emergency_contact', UserAPIView, basename='emergency_contact')

disease_router = NestedDefaultRouter(router, 'disease', lookup='user')
disease_router.register('disease', UserAPIView, basename='disease')

article_router = NestedDefaultRouter(router, 'article', lookup='user')
article_router.register('article', UserAPIView, basename='articles')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(emergency_contact_router.urls)),
    path('', include(disease_router.urls)),
    path('', include(article_router.urls)),
    
]