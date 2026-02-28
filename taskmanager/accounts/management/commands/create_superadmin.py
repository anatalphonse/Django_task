"""
Create superadmin user (default abcd/1234) if not present.
Usage: python manage.py create_superadmin
"""
import os
from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = "Create superadmin user (abcd/1234) if not present."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "abcd")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "1234")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"User '{username}' already exists."))
            return

        user = User.objects.create_superuser(username, email, password)
        user.role = "superadmin"
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Superadmin '{username}' created."))
