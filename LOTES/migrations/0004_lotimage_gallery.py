from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("LOTES", "0003_lot_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="LotImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.FileField(upload_to="lot_images/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "lot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="LOTES.lot",
                    ),
                ),
            ],
        ),
    ]
