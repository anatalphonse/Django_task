#!/usr/bin/env python
"""Create superadmin user (abcd/1234) if not present. Run after migrate."""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskmanager.settings")
django.setup()

from accounts.models import User

USERNAME = os.environ.get("DJANGO_SUPERUSER_USERNAME", "abcd")
PASSWORD = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "1234")
EMAIL = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    u = User.objects.get(username=USERNAME)
    u.role = "superadmin"
    u.save()
    print(f"Superadmin '{USERNAME}' created.")
else:
    print(f"User '{USERNAME}' already exists.")
