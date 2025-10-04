from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('teacher','Teacher'),
        ('student','Student')
    ]
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default="student")
    school = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name