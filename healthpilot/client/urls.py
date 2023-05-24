from django.conf.urls import include
from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .views import *

router = DefaultRouter()
router.register('users', UserAPIView, basename='users')
router.register('disease', DiseaseViewSet, basename='disease')
router.register('article', ArticleAPIView, basename='articles') #TODO some errors .validate() should return the validated data, AssertionError
router.register('emergency_contact', EmergencyContactAPIView, basename='emergency_contact')
router.register('users/(?P<users_id>[^/.]+)/users_emergency', UserEmergencyContactViewset, basename='user_emergency_contact')
router.register('doctors', DoctorViewSet, basename='doctors')
router.register(r'health_assessment_sections', HealthAssessmentSectionViewSet, basename='user_health_assessment')
router.register(r'medications', MedicationViewSet, basename='medications' )

# emergency_contact_router = NestedDefaultRouter(router, 'users', lookup='users')
# emergency_contact_router.register('users_emergency', UserEmergencyContactrViewset, basename='user_emergency_contact')


urlpatterns = [
    path('', include(router.urls)),
    path('payment/', PaymentCreateView.as_view(), name='payment'),
    path('profile/', UserProfileView.as_view(), name='profile'),

    
]