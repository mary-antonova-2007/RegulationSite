from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    user_folder = models.CharField(max_length=255, default='', blank=True)
    about = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
