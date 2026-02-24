from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_admin_user(apps, schema_editor):
    User = apps.get_model("USERS", "User")
    if not User.objects.filter(username="admin").exists():
        User.objects.create(
            username="admin",
            email="admin@example.com",
            role="ADMIN",
            is_staff=True,
            is_superuser=True,
            is_active=True,
            password=make_password("admin123"),
        )


class Migration(migrations.Migration):
    dependencies = [
        ("USERS", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]

