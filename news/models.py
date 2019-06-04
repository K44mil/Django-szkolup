from django.db import models
from users.models import MyUser
from django.urls import reverse
from tinymce import HTMLField


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    thumbnail = models.ImageField()
    title = models.CharField(max_length=100)
    overview = models.TextField()
    content = HTMLField('Content', default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'id': self.id
        })

    def get_update_url(self):
        return reverse('post-update', kwargs={
            'id': self.id
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'id': self.id
        })

class PostComment(models.Model):
    author_name = models.CharField(max_length=30)
    author_email = models.CharField(max_length=100)
    add_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class PostRate(models.Model):
    value = models.IntegerField(default=0)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
