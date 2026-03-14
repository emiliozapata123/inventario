from django.db import migrations
from django.contrib.auth.models import User
import os

def create_admin(apps, schema_editor):
    username = os.environ.get("SUPERUSER_NAME", "admin")
    email = os.environ.get("SUPERUSER_EMAIL", "admin@example.com")
    password = os.environ.get("SUPERUSER_PASSWORD", "12345678")
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),  # la nueva inicial
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]