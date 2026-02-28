# Task Manager - Django app
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Superadmin created on first run (override via env in docker-compose)
ENV DJANGO_SUPERUSER_USERNAME=abcd
ENV DJANGO_SUPERUSER_PASSWORD=1234
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (taskmanager project lives inside taskmanager/)
COPY taskmanager/ ./taskmanager/
WORKDIR /app/taskmanager

EXPOSE 8000

# Migrate, create superadmin (abcd/1234) if missing, then run server
# (create_superadmin may be skipped if user exists; server always starts)
CMD ["/bin/sh", "-c", "python manage.py migrate --noinput && (python manage.py create_superadmin || true) && exec python manage.py runserver 0.0.0.0:8000"]
