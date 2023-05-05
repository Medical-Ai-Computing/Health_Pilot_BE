from django.db import models
from django.utils import timezone
from datetime import date

class User(models.Model):
    nick_name=models.CharField(max_length=50, null=True, blank=True)
    full_name=models.CharField(max_length=50)

    date_of_birth=models.DateField()
    age = models.IntegerField(null=True, blank=True)

    joined_at=models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)
    deleted_at=models.DateTimeField(null=True, blank=True)

    CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    gender = models.CharField(choices=CHOICES, max_length=15, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length = 100, blank=True, null=True)
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

    def __str__(self):
        return f'{self.nick_name} => id {self.id}'