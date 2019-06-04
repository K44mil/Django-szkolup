from django.contrib import admin
from .models import MyUser, Student, Company

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Company)
admin.site.register(Student )