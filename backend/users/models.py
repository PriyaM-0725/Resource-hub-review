from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    # ✅ Academic fields (with defaults to avoid superuser error)
    branch = models.CharField(max_length=50, default='CSE')
    year = models.IntegerField(default=1)
    batch = models.CharField(max_length=20, default='2020-2024')
    regulation = models.CharField(max_length=20, default='R2021')

    def __str__(self):
        return self.username