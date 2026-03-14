import os
import django

# 1️⃣ Define la configuración
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_inventario.settings")
django.setup()

# 2️⃣ Ahora sí puedes importar User
from django.contrib.auth.models import User

# Datos del superusuario
USERNAME = os.environ.get("SUPERUSER_NAME", "admin")
EMAIL = os.environ.get("SUPERUSER_EMAIL", "admin@example.com")
PASSWORD = os.environ.get("SUPERUSER_PASSWORD", "12345678")

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print("Superuser creado correctamente")
else:
    print("El superuser ya existe")