from django.db import migrations
from django.contrib.auth.models import User

def create_admin(apps, schema_editor):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', '12345678')

class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),  # la anterior migración
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]