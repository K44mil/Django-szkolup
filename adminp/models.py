from django.db import models

# Create your models here.
class AdminMessage(models.Model):
	name = models.CharField(max_length=20)
	email = models.CharField(max_length=20)
	content = models.TextField()
	time = models.DateTimeField()
	read = models.BooleanField(default=False)
