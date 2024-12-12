from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_pics', blank=True)
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    
class Course(models.Model):
    name = models.CharField(max_length=200)
    teacher = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name
