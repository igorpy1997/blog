from django.contrib.auth.models import AbstractUser
from django.db import models





class Image(models.Model):
    IMAGE_TYPES = (
        ('header', 'Header Image'),
        ('profile', 'Profile Image'),
    )
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/')
    type = models.CharField(max_length=10, choices=IMAGE_TYPES)