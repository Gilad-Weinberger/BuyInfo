from django.db import models
from jsonfield import JSONField
import os

def profile_image_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    new_filename = f"profile_{instance.email}{ext}"
    return os.path.join('profile_images', new_filename)

class User(models.Model):
    first_name = models.CharField(max_length=60, null=True)
    last_name = models.CharField(max_length=60, null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=profile_image_upload_path
    )
    expenses = JSONField(default={})

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Family(models.Model):
    family_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=50)
    parents = models.ManyToManyField(User, related_name='parents')
    kids = models.ManyToManyField(User, related_name='kids')