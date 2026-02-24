from django.db import models

# Create your models here.
class Stage(models.Model):
    name = models.CharField(max_length=50)  # Lanzamiento, Preventa, etc.
    description = models.TextField()

class Lot(models.Model):
    STATUS_CHOICES = (
        ('AVAILABLE', 'Disponible'),
        ('RESERVED', 'Reservado'),
        ('SOLD', 'Vendido'),
    )

    code = models.CharField(max_length=20, unique=True)
    area_m2 = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.FileField(upload_to="lot_images/", blank=True, null=True)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AVAILABLE')

    # Para mapa interactivo
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.code


class LotImage(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="images")
    image = models.FileField(upload_to="lot_images/")
    created_at = models.DateTimeField(auto_now_add=True)
