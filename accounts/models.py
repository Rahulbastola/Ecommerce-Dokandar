
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Customer', 'Customer'),
        ('Vendor', 'Vendor'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Customer',
    )

    full_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
    )
