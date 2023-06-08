from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics, mixins, status, viewsets

import logging
from django.http import QueryDict
from django.utils import timesince, timezone
from .models import User, EmergencyContact, Disease, Article, Doctor, Payment, Membership, \
                    UserProfile, HealthAssessmentSection, Medication
from .serializers import UserSerializer, DiseaseSerializer, ArticleSerializer,\
                        EmergencyContactSerializer, DoctorsSerializer, PaymentSerializer, \
                        UserProfileSerializer, HealthAssessmentSectionSerializer, MedicationSerializer

class UserAPIView(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserProfileView(generics.RetrieveUpdateAPIView):
    '''Api View for users About Me section to Get, Post and Put request'''
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        if not self.request.user.is_authenticated:
            print('AuthenticationFailed usersssssss')
            raise AuthenticationFailed()
        
        user = self.request.user
        print(user, type(self.request.user), 'about me section---------------------')
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            print('user not found andddddddddddddddddddddd')
            # Create a new UserProfile object for the user if one doesn't exist
            return UserProfile.objects.create(user=user)

    def update(self, request, *args, **kwargs):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~update~~~~')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ArticleAPIView(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    '''Article to view and retrive including the rss feed which come 
        from other places/platform ------> we may crawel articles'''

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

class EmergencyContactAPIView(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    '''user can list create retrive and update and destroy emergency contacts'''

    serializer_class = EmergencyContactSerializer
    queryset = EmergencyContact.objects.all()

class UserEmergencyContactViewset(mixins.CreateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.ListModelMixin,
                                    GenericViewSet):
    '''user can list create retrive and update and destroy users/emergency contacts'''
    serializer_class = EmergencyContactSerializer
    # queryset = EmergencyContact.objects.all()
    lookup_field = 'patient'

    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs['users_id']
        
        try:
            emer_conn = User.objects.get(id=user_id)
            return EmergencyContact.objects.filter(patient=emer_conn).order_by('-created_at')
        except User.DoesNotExist:
            # object of type 'Response' has no len() error will occure if user not found
            return Response('User Not Found')
        

class DiseaseViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    serializer_class = DiseaseSerializer
    queryset = Disease.objects.all()


class DoctorViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    ''' api view method for doctors
    1. Create Doctors
    2. List doctors
    3. Retrive doctors
    4. Update
    5. Remove Doctors'''

    serializer_class = DoctorsSerializer
    queryset = Doctor.objects.all()

class PaymentCreateView(generics.CreateAPIView):
    '''used to process the payment'''
    # permission_classes = [IsAuthenticated] # authenticated users can have editable forms
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        print('before request data', request.data['user'], request.data)
        # membership_type = request.user.membership.membership_type
        membership_type = User.objects.get(id=request.data['user']).membership

        if membership_type == 'F':
            # request.user.membership.membership_type = 'premium'
            # request.user.membership.save()
            print('---------- membership type is Free----------')

            user_id = request.data['user']
            print(user_id, 'user--id--id')
            membership = Membership() # user.membership
            membership.activate_premium_membership()
        else:
            message = 'This user is already Premium user'
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, *args, **kwargs)
        #TODO try to add 400 bad request up here if the payment not successfull

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        serializer.instance.is_paid = True
        serializer.instance.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HealthAssessmentSectionViewSet(viewsets.ModelViewSet):
    #TODO only get_queryset and retrive function by user_id
    serializer_class = HealthAssessmentSectionSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        queryset = HealthAssessmentSection.objects.filter(delete_health_profiles_option=False)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        queryset = queryset.order_by('-created_at')
        return queryset # TODO add exception if user does not exist
    
    def retrieve(self, request, *args, **kwargs):
        # to access this endpoint pass /?user_id=<id>
        try:
            self.user = User.objects.get(id=kwargs['pk'], 
                                         deleted_at=None)
        except User.DoesNotExist:
            return Response("User Does Not Exist.", 
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = HealthAssessmentSection.objects.filter(user=self.user ,
                                                              delete_health_profiles_option=False)
        except HealthAssessmentSection.DoesNotExist:
            return Response('Health History not recorded in the system. please have one health history', 
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class MedicationViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationSerializer
    queryset = Medication.objects.all()

    def perform_create(self, serializer):
        medication = serializer.save()

        # Send medication reminder email
        subject = 'Medication Reminder'
        message = f"Don't forget to take your medication: {medication.name}"
        send_mail(subject, message, 'spyxmeni@gmail.com', [self.request.user.email])

    def perform_update(self, serializer):
        medication = serializer.save()

        # Check if medication is ongoing and send reminder if needed
        if medication.start_date <= timezone.now().date() and (medication.end_date is None or medication.end_date >= timezone.now().date()):
            subject = 'Medication Reminder'
            message = f"Don't forget to take your medication: {medication.name}"
            send_mail(subject, message, 'spyxmeni@gmail.com', [self.request.user.email])


# class RateReviewView(View):
#     def post(self, request, consultation_id):
#         consultation_obj = consultation.objects.get(id=consultation_id)
#         patient = consultation_obj.patient
#         doctor1 = consultation_obj.doctor
#         rating = request.POST.get('rating')
#         review = request.POST.get('review')

#         rating_obj = rating_review(patient=patient, doctor=doctor1, rating=rating, review=review)
#         rating_obj.save()

#         rate = int(rating_obj.rating_is)
#         doctor.objects.filter(pk=doctor1).update(rating=rate)

#         return redirect('consultationview', consultation_id)