from django.conf.urls import include
from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .views import *

router = DefaultRouter()
router.register('users', UserAPIView, basename='users')
router.register('disease', DiseaseViewSet, basename='disease')
router.register('article', UserAPIView, basename='articles')
router.register('emergency_contact', UserAPIView, basename='emergency')
router.register('doctors', DoctorViewSet, basename='doctors')


emergency_contact_router = NestedDefaultRouter(router, 'users', lookup='user')
emergency_contact_router.register('emergency_contact', EmergencyContactAPIView, basename='emergency_contact')

disease_router = NestedDefaultRouter(router, 'users', lookup='user')
disease_router.register('disease', DiseaseViewSet, basename='disease')

article_router = NestedDefaultRouter(router, 'users', lookup='user')
article_router.register('article', ArticleAPIView, basename='articles')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(emergency_contact_router.urls)),
    path('', include(disease_router.urls)),
    path('', include(article_router.urls)),
    path('payment/', PaymentCreateView.as_view(), name='payment'),
    
]