from django.db.models import Q
from .models import User, Article, Disease, EmergencyContact, Category, \
                    Doctor, Payment , UserProfile, HealthAssessmentSection, Medication
from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

class UserSerializer(serializers.ModelSerializer):
    '''Used to get and update users'''
    class Meta:
        model = User
        fields = ['id','username', 'full_name', 'gender', 'email', 'date_of_birth',
                  'weight', 'height', 'membership', 'mobile_no', 'address', 'country'] #  'country', object not serializable fix it maybe by get_queryset
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user','about_me']

        def validate_about_me(self, value):
            """
            Truncate the 'about_me' field if it is too long.
            """
            max_length = UserProfile._meta.get_field('about_me').max_length
            if len(value) > max_length:
                value = value[:max_length]
            return value

class EmergencyContactSerializer(serializers.ModelSerializer):
    '''used to get information of emergency contacts'''
    class Meta:
        model = EmergencyContact
        fields = ['first_name', 'last_name', 'relationship', 'address', 
                   'email', 'cell_phone', 'patient']

class CategorySerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='name')

    class Meta:

        model = Category
        fields = ['category', 'name']

class ArticleSerializer(serializers.ModelSerializer):
    '''get article and post from craweld data or create a new'''
    class Meta:
        model = Article
        fields = ['article_id', 'author', 'categories', 'tags', 'created_at', 'updated_at']
    def validate(self, attrs):
        pass
        # return super().validate(attrs)

    # def get_categories(self, obj):
    # '''obj is an agent instance.'''

    #     qset = Category.objects.filter(name=obj)
    #     return [CategorySerializer(m).data for m in qset]

class DiseaseSerializer(serializers.ModelSerializer):
    '''serialize Disease of users'''
    class Meta:
        model = Disease
        fields = ['patient', 'disease_name', 'no_of_symp', 'symptoms_name', 
                  'confidence', 'consultdoctor', 'allargis', 'blood_type', 'blood_pressure',
                   'chronic_condition', 'smoke', 'alcohol', 'recent_surgeries', 'infectious_diseases', 'is_pregnant' ]

class DoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['doctor_name', 'doctor_type', 'email', 'cell_phone', 'patient']
        
# payment serializers
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'amount', 'payment_method', 'is_paid']
    
class HealthAssessmentSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthAssessmentSection
        fields = ['user', 'health_tracking_history', 'symptom_history', 'recommended_history', 'created_at']

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'