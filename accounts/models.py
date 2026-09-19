from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    display_name = models.CharField(max_length=100, blank=True)
    education_level = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. High School, Undergraduate, Postgraduate",
    )
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name or self.username