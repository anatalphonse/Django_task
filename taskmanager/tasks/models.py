from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.
User = settings.AUTH_USER_MODEL

class Task(models.Model):

  STATUS_CHOICES = (
    ("pending","Pending"),
    ("progress","In Progress"),
    ("completed","Completed"),
  )

  title = models.CharField(max_length=255)
  description = models.TextField()
  assigned_to = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="tasks",
  )

  due_date = models.DateField()

  status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='pending'
  )

  completion_report = models.TextField(null=True, blank=True)
  worked_hours = models.FloatField(null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title
  
  def clean(self):
    if self.status == "completed":
      if not self.completion_report or not self.worked_hours:
        raise ValidationError("RePort and worked hours required when completing task")