from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment


@receiver(post_save, sender=Payment)
def noop_payment_signal(sender, instance, created, **kwargs):
    return
