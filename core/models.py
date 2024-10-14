from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20)

    def __str__(self):
        """self.user.username"""
        return str(self.user.username)
    
