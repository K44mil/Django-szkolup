from django.db import models
from django.urls import reverse
from users.models import Student, Company, MyUser

# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    start_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    max_students = models.IntegerField(default=0)
    has_certificate = models.BooleanField(default=False)
    thumbnail = models.ImageField()
    views_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course-details', kwargs={
            'id': self.id
        })

    def get_save_student_url(self):
        return reverse('course-save', kwargs={
            'id': self.id
        })

    def get_delete_url(self):
        return reverse('course-delete', kwargs={
            'id': self.id
        })

class CourseComment(models.Model):
    author_name = models.CharField(max_length=30)
    author_email = models.CharField(max_length=100)
    add_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class CourseRate(models.Model):
    value = models.IntegerField(default=0)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)