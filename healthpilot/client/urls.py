from django.conf.urls import include
from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .views import *

router = DefaultRouter()
router.register('users', UserAPIView, basename='users')
router.register('disease', DiseaseViewSet, basename='disease')
router.register('article', ArticleAPIView, basename='articles')
router.register('emergency_contact', EmergencyContactAPIView, basename='emergency_contact')
router.register('users/(?P<users_id>[^/.]+)/users_emergency', UserEmergencyContactViewset, basename='user_emergency_contact')
router.register('user_doctors', UserDoctorViewSet, basename='user_doctors')
router.register('users/(?P<users_id>[^/.]+)/user_doctors', SingleUserDoctorViewset, basename='user_doctors_list')
router.register('health_assessment_sections', HealthAssessmentSectionViewSet, basename='user_health_assessment')
router.register('medications', MedicationViewSet, basename='medications' )
router.register('profile', UserProfileViewSet, basename='profile')


urlpatterns = [
    path('', include(router.urls)),
    path('payment/', PaymentCreateView.as_view(), name='payment'),

]