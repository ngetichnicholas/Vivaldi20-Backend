from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profession = models.CharField(max_length=100, default="AWS Cloud Practitioner")
    bio = models.TextField(blank=True, default="No bio provided")
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.username
