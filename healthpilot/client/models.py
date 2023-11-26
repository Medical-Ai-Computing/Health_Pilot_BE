from django.db import models
from django.utils import timezone
from django.db.models.query_utils import Q
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from datetime import date

class User(models.Model):
    first_name=models.CharField(max_length=50, null=True)
    last_name=models.CharField(max_length=50, null=True)
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

    membership=models.CharField(choices=MEMBERSHIP_FIELD, null=True,  #TODO make the default free
                                blank=True, default='Free', max_length=1)

    gender = models.CharField(choices=CHOICES, max_length=15, 
                              null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length = 250, blank=True, null=True)
    mobile_no = models.CharField(max_length = 15, blank=True, null=True)
    country = models.CharField(blank=True, null=True)

    bmi = models.FloatField(blank=True, null=True) # Body mass index
    bpm = models.IntegerField(blank=True, null=True, default='120')
    sleep_time = models.FloatField(blank=True, null=True, default='8')

    def save(self, *args, **kwargs):
        # Calculate BMI before saving the user
        if self.weight and self.height:
            self.bmi = self.calculate_bmi()
        super().save(*args, **kwargs)

    def calculate_bmi(self):
        # BMI formula: weight (kg) / (height (m) ^ 2)
        height_in_meters = self.height / 100  # Convert height to meters
        return self.weight / (height_in_meters ** 2)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['email', 'first_name', 'last_name'], name='unique_name_and_email'),
        models.UniqueConstraint(fields=['email'], name='unique email', condition=(~Q(email=''))),
    ]
        
    def __str__(self):
        return f'{self.first_name} => id {self.id}'

class UserProfile(models.Model):
    '''user profile about me section'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    about_me = models.CharField(max_length=255 ,blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)

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
    disease_name = models.CharField(max_length = 200, null=True)
    # no_of_symp = models.IntegerField()
    symptoms_name = models.CharField(max_length=300, null=True)
    # confidence = models.DecimalField(max_digits=5, decimal_places=2)
    consultdoctor = models.CharField(max_length = 200, default='No')
    allargis = models.CharField(max_length=400, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    # basic question with choices fileds
    blood_type = models.CharField(max_length=11, choices=BLOOD_TYPE_CHOICES, null=True, default='DK')
    hypertension = models.CharField(max_length=2, choices=CHOICES,  default='') # high blood presure
    chronic_condition = models.CharField(max_length=2, choices=CHOICES, default='N') # diabti,..
    smoke = models.CharField(max_length=2, choices=CHOICES, default='N')
    alcohol = models.CharField(max_length=2, choices=CHOICES, default='N')
    recent_surgeries = models.CharField(max_length=2, choices=CHOICES, default='N')
    good_sleep_pattern = models.CharField(max_length=2, choices=CHOICES, default='N')
    infectious_diseases = models.CharField(max_length=2, choices=CHOICES, default='N')
    is_pregnant = models.CharField(max_length=2, choices=CHOICES, default='N')


    def __str__(self):
        return 'f{self.patient} -> {self.disease_name}'
    
class Category(models.Model):
    '''catagory of the article for recommendation system'''
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
    name = models.CharField(max_length=250)
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class Article(models.Model): # comment, like count, users(who commented)

    '''Article including the rss feed which come 
    from other places/platform ------> we may crawel articles'''

    # article_id=models.IntegerField(unique=True) # article id must be unique
    author = models.CharField(max_length=250, default='WHO')
    categories = models.ManyToManyField(
        Category, related_name='articles',  blank=True)
    link = models.CharField(max_length=250, blank=True)
    keywords = models.CharField(blank=True, null=True)
    headline = models.TextField(null=True, blank=True, unique=True)
    body = models.TextField(null=True)
    image_url = models.CharField(blank=True, null=True)
    read_time = models.CharField(null=True, blank=1, default='1')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    total_comment= models.PositiveIntegerField(default=0, null=True, blank=True)
    total_like=models.PositiveIntegerField(default=0, null=True, blank=True)


    def __str__(self):
        return str(self.id)
    
class Interaction(models.Model):
    LIKE = 'like'
    COMMENT = 'comment'
    
    INTERACTION_CHOICES = [
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES)
    text = models.TextField(blank=True, null=True)
    parent_interaction = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

class PatientDoctor(models.Model):
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
   
    INFO_SEND_OPITION=[('D','Daily'),('W','weekly'),
                       ('M','Monthly'),('BW','Bi-weekly')]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    doctor_type = models.CharField(choices=SPECIALIZATION_CHOICES, max_length=5, default='OTHER', blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    cell_phone=models.CharField(max_length=15, null=True)
    patient = models.ForeignKey(User , null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    sent_frequency = models.CharField(choices=INFO_SEND_OPITION, default='M')

    def __str__(self):
        for choice in self.SPECIALIZATION_CHOICES:
            if choice[0] == self.SPECIALIZATION_CHOICES:
                return f"Dr. {self.first_name + '' + self.last_name} ({choice[1]})"
        return f"{self.first_name} (Other Specialty)"
    
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
        self.end_date.save()

    def __str__(self):
        return f"{self.user.first_name}'s membership {self.membership_type}"

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
    health_tracking_history = models.TextField(default='')
    symptom_history = models.TextField(null=False, default='')
    recommended_history = models.TextField(null=False)
    delete_health_profiles_option = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"HealthAssessmentSection ({self.user})"
    
class Medication(models.Model):
    '''adding medication for a user with reminders and 
        incorporating it into the user's health assessment story.'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    medication_name = models.CharField(max_length=100) # medication name
    how_much_dosage = models.CharField(max_length=50, null=True) # how many in mili-gram
    intake_per_day = models.CharField(max_length=50) # usage perday
    start_date = models.DateField(auto_now=True, null=True)  #TODO on the mobile app add this field
    end_date = models.DateField(null=True, blank=True) # opitional field

    def clean(self):
        super().clean()
        if self.start_date > timezone.now().date():
            raise ValidationError("Start date cannot be in the future.")
        
    def save(self, *args, **kwargs):
        self.clean()  # Run full validation before saving
        super().save(*args, **kwargs)
 
    def __str__(self):
        return self.name
    
class Language_Preference(models.Model):
    """api used to store users prefered language"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user + self.language


# the blow code is for future and premium users
# class Doctor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
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
