from django.contrib import admin
from .models import Course, City, Category, Subcategory, Region, CourseRate
# Register your models here.

admin.site.register(Course)
admin.site.register(City)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Region)
admin.site.register(CourseRate)
