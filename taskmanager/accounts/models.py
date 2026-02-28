from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
  ROLE_CHOICES = (
    ("superadmin","SuperAdmin"),
    ("admin","Admin"),
    ("user","User"),
  )

  role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

  admin = models.ForeignKey(
    "self",
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    limit_choices_to={'role': 'admin'}
  )

  def __str__(self):
    return f"{self.username} ({self.role})"
