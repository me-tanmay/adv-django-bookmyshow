from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('user', 'User'),
        ('event_manager', 'Event Manager'),
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')

    def __str__(self):
        return self.email
