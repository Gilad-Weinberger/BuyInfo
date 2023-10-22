from django.db import models
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []