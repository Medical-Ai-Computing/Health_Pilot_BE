from django.conf.urls import include
from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .views import *

router = DefaultRouter()
router.register('users', UserAPIView, basename='users')
router.register('disease', DiseaseViewSet, basename='disease')
router.register('article', ArticleAPIView, basename='articles')
router.register('emergency_contact', EmergencyContactAPIView, basename='emergency')
router.register('doctors', DoctorViewSet, basename='doctors')


emergency_contact_router = NestedDefaultRouter(router, 'emergency_contact', lookup='emergency_contact')
emergency_contact_router.register('emergency_contact', EmergencyContactAPIView, basename='emergency_contact')

disease_router = NestedDefaultRouter(router, 'disease', lookup='disease')
disease_router.register('disease', DiseaseViewSet, basename='disease')

article_router = NestedDefaultRouter(router, 'article', lookup='article')
article_router.register('article', ArticleAPIView, basename='articles') #TODO some errors


urlpatterns = [
    path('', include(router.urls)),
    path('', include(emergency_contact_router.urls)),
    path('', include(disease_router.urls)),
    path('', include(article_router.urls)),
    path('payment/', PaymentCreateView.as_view(), name='payment'),
    
]