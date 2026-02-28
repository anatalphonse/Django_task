from rest_framework import serializers
from .models import Task

class TaskSerializar(serializers.ModelSerializer):
  class Meta:
    model = Task 
    fields = "__all__"
    read_only_fields = ["assigned_to"]