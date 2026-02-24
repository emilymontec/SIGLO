from decimal import Decimal

from django.db import migrations
from django.db.models import Sum


def sync_lot_statuses(apps, schema_editor):
    Purchase = apps.get_model("SALES", "Purchase")
    Payment = apps.get_model("SALES", "Payment")
    Lot = apps.get_model("LOTES", "Lot")

    lot_status_map = {}

    for purchase in Purchase.objects.all():
        lots = list(purchase.lots.all())
        if not lots:
            continue

        total = purchase.total_amount or Decimal("0")
        total_paid = (
            Payment.objects.filter(purchase=purchase).aggregate(s=Sum("amount"))["s"]
            or Decimal("0")
        )
        is_fully_paid = total > Decimal("0") and total_paid >= total
        status = "SOLD" if is_fully_paid else "RESERVED"

        for lot in lots:
            previous_status = lot_status_map.get(lot.id)
            if previous_status is None or status == "SOLD":
                lot_status_map[lot.id] = status

    for lot in Lot.objects.all():
        new_status = lot_status_map.get(lot.id)
        if new_status is None:
            lot.status = "AVAILABLE"
        else:
            lot.status = new_status
        lot.save()


class Migration(migrations.Migration):

    dependencies = [
        ("SALES", "0002_initial"),
        ("LOTES", "0003_lot_image"),
    ]

    operations = [
        migrations.RunPython(sync_lot_statuses, migrations.RunPython.noop),
    ]

