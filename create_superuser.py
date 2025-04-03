# create_superuser.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Check if a superuser already exists
username = os.getenv("DJANGO_SUPERUSER_EMAIL", "abdelaali@1337.ma")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "abdelaali@1337.ma")
if not User.objects.filter(
    is_superuser=True,
    email=username,
).exists():
    User.objects.create_superuser(
        username=username,
        email=username,
        password=password,
    )
    print("Superuser created successfully!")
else:
    print("Superuser already exists. Skipping creation.")
