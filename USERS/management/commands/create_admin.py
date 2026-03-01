import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

class Command(BaseCommand):
    help = 'Crea el usuario administrador automáticamente desde el archivo .env'

    def handle(self, *args, **options):
        load_dotenv()
        
        User = get_user_model()
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        if not username or not email or not password:
            self.stdout.write(self.style.ERROR('Faltan variables de entorno para el administrador en el archivo .env'))
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role='ADMIN' # Aseguramos que tenga el rol de ADMIN
            )
            self.stdout.write(self.style.SUCCESS(f'Usuario administrador "{username}" creado exitosamente.'))
        else:
            self.stdout.write(self.style.WARNING(f'El usuario administrador "{username}" ya existe.'))
