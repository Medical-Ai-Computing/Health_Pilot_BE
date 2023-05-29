from django.db import models
from django.utils import timezone
from django.db.models.query_utils import Q
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from datetime import date

class User(AbstractUser):
    # user = models.IntegerField()
    username=models.CharField(max_length=50, null=True, blank=True)
    full_name=models.CharField(max_length=50)
    
    password = models.CharField(max_length=128, default='1234')
    date_of_birth=models.DateField(null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    # weight in kilogram
    weight = models.FloatField(default=0)
    #store user hegith in CentiMeter
    height = models.FloatField(default=0)

    joined_at=models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)
    deleted_at=models.DateTimeField(null=True, blank=True)

    MEMBERSHIP_FIELD = [('F', 'Free'), ('P','Premium')]
    CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    membership=models.CharField(choices=MEMBERSHIP_FIELD, null=True, blank=True, default='F', max_length=1)

    gender = models.CharField(choices=CHOICES, max_length=15, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length = 250, blank=True, null=True)
    mobile_no = models.CharField(max_length = 15, blank=True, null=True)
    country = models.CharField(blank=True, null=True)
    # country = CountryField(blank=True, null=True, blank_label="(Select country)")

    @property
    def age(self):
        today = date.today()
        db = self.date_of_birth
        age = today.year - db.year
        if today.month < db.month or today.month == db.month and today.day < db.day:
            age -= 1
        return age

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['email', 'username'], name='unique name and email in a community'),
        models.UniqueConstraint(fields=['email'], name='unique email', condition=(~Q(email=''))),
        models.UniqueConstraint(fields=['username'], name='user_name must be unique')
    ]
        
    def __str__(self):
        return f'{self.username} => id {self.id}'

class UserProfile(models.Model):
    '''user profile about me section'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    about_me = models.CharField(max_length=255 ,blank=True)

    def __str__(self):
        return f'{self.user} about me'

class EmergencyContact(models.Model):
    '''emergency contact information of users'''
    RELATION_SHIP =[('MOTHER', 'Mother'),
                    ('FATHER', 'Father'),
                    ('PARENT', 'Parent'),
                    ('BROTHER', 'Brother'),
                    ('SISTER', 'Sister'),
                    ('SON', 'Son'),
                    ('DAUGHTER', 'Daughter'),
                    ('CHILD', 'Child'),
                    ('FRIEND', 'Friend'),
                    ('SPOUSE', 'Spouse'),
                    ('ASSISTANT', 'Assistant'),
                    ('MANAGER', 'Manager'),
                    ('ROOMMATE', 'Roommate'),
                    ('DOCTOR', 'Doctor'),
                    ('OTHER', 'Other')]
    
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    relationship=models.CharField(choices=RELATION_SHIP, max_length=15)
    address=models.CharField(max_length=250)
    email=models.EmailField(blank=True, null=True)
    cell_phone=models.CharField(max_length=15, null=True)
    patient = models.ForeignKey(User , null=True, on_delete=models.SET_NULL, related_name='emergency_contacts')
    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        # Check if the user already has three emergency contacts
        existing_contacts = EmergencyContact.objects.filter(patient=self.patient)
        if existing_contacts.count() >= 3:
            raise ValidationError("A user can have only two emergency contacts.")
    
    def save(self, *args, **kwargs):
        self.clean()  # Run full validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return '{first_name} {last_name} for {patient}'
    
class Disease(models.Model):
    '''Dieases information for users'''
    BLOOD_TYPE_CHOICES= [
                        ('A_POSITIVE', 'A+'),
                        ('A_NEGATIVE', 'A-'),
                        ('B_POSITIVE', 'B+'),
                        ('B_NEGATIVE', 'B-'),
                        ('AB_POSITIVE', 'AB+'),
                        ('AB_NEGATIVE', 'AB-'),
                        ('O_POSITIVE', 'O+'),
                        ('O_NEGATIVE', 'O-'),
                        ('DK','i Dont Know')]
    CHOICES = [
            ('Y', 'Yes'),
            ('N', 'No'),
            ('DK', "I don't know")]

    patient = models.ForeignKey(User , null=True, on_delete=models.SET_NULL)
    disease_name = models.CharField(max_length = 200)
    no_of_symp = models.IntegerField()
    symptoms_name = models.CharField(max_length=300)
    confidence = models.DecimalField(max_digits=5, decimal_places=2)
    consultdoctor = models.CharField(max_length = 200)
    allargis = models.CharField(max_length=400, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    # basic question with choices fileds
    blood_type = models.CharField(max_length=11, choices=BLOOD_TYPE_CHOICES, null=True, default='DK')
    blood_pressure = models.CharField(max_length=2, choices=CHOICES,  default='N')
    chronic_condition = models.CharField(max_length=2, choices=CHOICES, default='N')
    smoke = models.CharField(max_length=2, choices=CHOICES, default='N')
    alcohol = models.CharField(max_length=2, choices=CHOICES, default='N')
    recent_surgeries = models.CharField(max_length=2, choices=CHOICES, default='N')
    infectious_diseases = models.CharField(max_length=2, choices=CHOICES, default='N')
    #TODO i want to ask the user pregenancy based on gender type
    is_pregnant = models.CharField(max_length=2, choices=CHOICES, default='N')

    def save(self, *args, **kwargs):
        if self.patient.gender == 'Male':
            self.is_pregnant = False
            super().save(*args, **kwargs)

    def __str__(self):
        return "f{patient} - > {disease_name}"
    
class Category(models.Model):
    '''catagory of the artcile for recommendation system'''
    category = models.IntegerField()
    # article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
    
class Tag(models.Model):
    '''Tag of the article for recommendation system'''
    tag = models.IntegerField()
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Article(models.Model):

    '''Article including the rss feed which come 
    from other places/platform ------> we may crawel articles'''

    article_id=models.IntegerField()
    author = models.CharField(max_length=250)
    categories = models.ManyToManyField(
        Category, related_name='articles',  blank=True)
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.article_id)
    
class Doctor(models.Model):
    '''used to send the health report of users to selected doctors
    and this is the doctor contact information'''

    SPECIALIZATION_CHOICES = [('AN', 'Anesthesiologist'), ('CA', 'Cardiologist'),
                              ('DE', 'Dermatologist'),    ('EN', 'Endocrinologist'),
                              ('FA', 'Family medicine'),  ('GA', 'Gastroenterologist'),
                              ('GE', 'Geriatrician'),     ('HA', 'Hematologist'),
                              ('IM', 'Internal medicine'),('IMM', 'Immunologist'),
                              ('NE', 'Nephrologist'),     ('NEU', 'Neurologist'),
                              ('OB', 'Obstetrics and gynaecology'),
                              ('ON', 'Oncologist'),       ('OP', 'Ophthalmology'),
                              ('PA', 'Pathologist'),      ('PD', 'Pediatrician'),
                              ('PE', 'Pediatrics'),       ('PS', 'Psychiatrist'),
                              ('PU', 'Pulmonologist'),    ('RA', 'Radiologist'),
                              ('RH', 'Rheumatologist'),   ('SU', 'Surgeon'),
                              ('UR', 'Urologist'),        ('OTHER', 'Other')]
    
    doctor_name = models.CharField(max_length=100)
    doctor_type = models.CharField(choices=SPECIALIZATION_CHOICES, max_length=5, default='OTHER', blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    cell_phone=models.CharField(max_length=15, null=True)
    patient = models.ForeignKey(User , null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        for choice in self.SPECIALIZATION_CHOICES:
            if choice[0] == self.SPECIALIZATION_CHOICES:
                return f"Dr. {self.doctor_name} ({choice[1]})"
        return f"{self.doctor_name} (Other Specialty)"
    
# the down code is for payment and membership status

class Payment(models.Model):
    PAYMENT_CHOICES =  [('bank', 'Bank Transfer'),
                        ('paypal', 'PayPal'),
                        ('creditcard', 'Credit Card')]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships_payment')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    is_paid = models.BooleanField(default=False)

class Membership(models.Model):
    MEMBERSHIP_FIELD = [('F', 'Free'), ('P','Premium')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='memberships')
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_FIELD,  default='Free')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def activate_premium_membership(self):
        '''membership active period is 30 days or 1 month'''
        self.membership_type = 'Premium'
        self.end_date = timezone.now() + timezone.timedelta(days=30) 
        self.save()

    def __str__(self):
        return f"{self.user.username}'s membership {self.membership_type}"

class AdditionalFeatures(models.Model):
    '''a model for addition features such as notification and reminders'''
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    medication_reminders = models.BooleanField(default=False)
    language_translation_services = models.BooleanField(default=False)
    communication_with_healthcare_providers = models.BooleanField(default=False)
    useful_health_tips_and_articles = models.BooleanField(default=False)
    wearable_integration = models.BooleanField(default=False)
    virtual_consultations = models.BooleanField(default=False)
    appointment_scheduling = models.BooleanField(default=False)
    health_coaching_services = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Users Feature ({self.patient})"

class HealthAssessmentSection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    health_tracking_history = models.TextField()
    recommended_history = models.TextField()
    delete_health_profiles_option = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"HealthAssessmentSection ({self.id})"
    
class Medication(models.Model):
    '''adding medication for a user with reminders and 
        incorporating it into the user's health assessment story.'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def clean(self):
        super().clean()
        if self.start_date > timezone.now().date():
            raise ValidationError("Start date cannot be in the future.")
        
    def save(self, *args, **kwargs):
        self.clean()  # Run full validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


# the blow code is for future and premium users
# class Doctor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     full_name = models.CharField(max_length=100)
#     date_of_birth = models.DateField()
#     joined_at=models.DateTimeField(auto_now_add=True)
#     deleted_at=models.DateTimeField(null=True, blank=True)

#     CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

#     gender = models.CharField(choices=CHOICES, max_length=15, null=True, blank=True)
#     email = models.EmailField(blank=True, null=True)
#     address = models.CharField(max_length = 250, blank=True, null=True)
#     mobile_no = models.CharField(max_length = 15, blank=True, null=True)
#     country = CountryField(blank=True, null=True, blank_label="(Select country)")

#     # doctor rating by users
#     # rating = models.IntegerField(default=0)

# class Consultation(models.Model):
#     '''a class for premium users to have and consult doctors'''

#     patient = models.ForeignKey(User ,null=True, on_delete=models.SET_NULL)
#     doctor = models.ForeignKey(Doctor ,null=True, on_delete=models.SET_NULL)
#     disease = models.OneToOneField(Disease, null=True, on_delete=models.SET_NULL)
#     consultation_date = models.DateField()
#     status = models.CharField(max_length = 20)

# class Rating_Review(models.Model):
#     '''class for the doctors rating to appear in his
#        profile so that user can choise a good doctors'''
    
#     patient = models.ForeignKey(User ,null=True, on_delete=models.SET_NULL)
    # doctor = models.ForeignKey(Doctor ,null=True, on_delete=models.SET_NULL)
    
    # rating = models.IntegerField(default=0)
    # review = models.TextField(blank=True) 


    # @property
    # def rating_is(self):
    #     new_rating = 0
    #     rating_obj = Rating_Review.objects.filter(doctor=self.doctor)
    #     for i in rating_obj:
    #         new_rating += i.rating
       
    #     new_rating = new_rating/len(rating_obj)
    #     new_rating = int(new_rating)
        
    #     return new_rating