from django.db import migrations
from django.contrib.auth.hashers import make_password
import os


def create_admin_user(apps, schema_editor):
    User = apps.get_model("USERS", "User")
    
    # Obtener credenciales de variables de entorno con valores por defecto
    admin_username = os.environ.get("ADMIN_USERNAME")
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")
    
    if not User.objects.filter(username=admin_username).exists():
        User.objects.create(
            username=admin_username,
            email=admin_email,
            role="ADMIN",
            is_staff=True,
            is_superuser=True,
            is_active=True,
            password=make_password(admin_password),
        )


class Migration(migrations.Migration):
    dependencies = [
        ("USERS", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]

