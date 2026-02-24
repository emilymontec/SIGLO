from django.db import models
from django.conf import settings
from LOTES.models import Lot


class Purchase(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lots = models.ManyToManyField(Lot)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def balance(self):
        total_paid = sum(p.amount for p in self.payment_set.all())
        return self.total_amount - total_paid


class Payment(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
