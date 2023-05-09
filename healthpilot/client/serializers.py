from django.db.models import Q
from .models import User, Article, Disease, EmergencyContact, Category, Doctor
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    '''Used to get and update users'''
    class Meta:
        model = User
        fields = ['id','username', 'full_name', 'date_of_birth', 'age', 'gender', 'membership']
        read_only_fields = ['id']

class EmergencyContactSerializer(serializers.ModelSerializer):
    '''used to get information of emergency contacts'''
    class Meta:
        model = EmergencyContact
        fileds = ['first_name', 'last_name', 'relationship', 'address', 'email', 'cell_phone', 'patient']

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
        fields = ['patient', 'disease_name', 'no_of_symp', 'symptoms_name', 'confidence', 'consultdoctor', 'allargis' ]

class DoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['doctor_name', 'doctor_type', 'email', 'cell_phone', 'patient']
