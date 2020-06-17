from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_picture = models.ImageField(blank=True, upload_to='profile_pictures')
    portfolio_site = models.URLField(blank=True)

    def __str__(self):
        return self.user.username
