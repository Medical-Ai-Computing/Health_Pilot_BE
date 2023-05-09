from django.db import models
from django.utils import timezone
from django.db.models.query_utils import Q
from django.contrib.postgres.fields import ArrayField
from datetime import date

class User(models.Model):
    username=models.CharField(max_length=50, null=True, blank=True)
    full_name=models.CharField(max_length=50)

    date_of_birth=models.DateField()
    age = models.IntegerField(null=True, blank=True)

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
    country = models.CharField(max_length=25, blank=True, null=True)

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
                    ('PARTNER', 'Parent'),
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
    patient = models.ForeignKey(User , null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return '{first_name} {last_name} for {patient}'
    
class Disease(models.Model):
    '''Dieases information for users'''
    patient = models.ForeignKey(User , null=True, on_delete=models.SET_NULL)

    disease_name = models.CharField(max_length = 200)
    no_of_symp = models.IntegerField()
    symptoms_name = ArrayField(models.CharField(max_length=300))
    confidence = models.DecimalField(max_digits=5, decimal_places=2)
    consultdoctor = models.CharField(max_length = 200)
    allargis = models.CharField(max_length=400, null=True, blank=True)
    # created_at = models.DateTimeField(default=timezone.now)

class Category(models.Model):
    '''catagory of the artcile for recommendation system'''
    category = models.IntegerField()
    # article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)
    
class Tag(models.Model):
    '''Tag of the article for recommendation system'''
    tag = models.IntegerField()
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
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