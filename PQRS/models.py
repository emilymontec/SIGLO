from django.db import models

# Create your models here.
from django.conf import settings

class PQRS(models.Model):
    TYPE_CHOICES = (
        ('P', 'Petición'),
        ('Q', 'Queja'),
        ('R', 'Reclamo'),
        ('S', 'Sugerencia'),
    )

    STATUS_CHOICES = (
        ('OPEN', 'Abierto'),
        ('CLOSED', 'Cerrado'),
    )

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')