from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
    role = models.IntegerField(default=0)
    isProfilEdited = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.username

class Student(models.Model):
    name = models.CharField(max_length=50, default='')
    surname = models.CharField(max_length=50, default='')
    email = models.CharField(max_length=127, default='')
    city = models.CharField(max_length=127, blank=True, null=True, default='')
    street = models.CharField(max_length=127, blank=True, null=True, default='')
    house_number = models.CharField(max_length=20, blank=True, null=True, default='')
    flat_number = models.CharField(max_length=20, blank=True, null=True, default='')
    user = models.ForeignKey(MyUser, models.DO_NOTHING)

    def __str__(self):
        return str(self.name) + " " + str(self.surname)

class Company(models.Model):
    company_name = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=127, default='')
    street = models.CharField(max_length=127, blank=True, null=True, default='')
    house_number = models.CharField(max_length=20, default='')
    flat_number = models.CharField(max_length=20, blank=True, null=True, default='')
    email = models.CharField(max_length=127, default='')
    user = models.ForeignKey(MyUser, models.DO_NOTHING)

    def __str__(self):
        return self.company_name