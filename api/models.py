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