from django.db import migrations


def create_default_stages(apps, schema_editor):
    Stage = apps.get_model("LOTES", "Stage")

    defaults = [
        (
            "Lanzamiento",
            "Etapa inicial del proyecto, con oferta limitada y precios preferenciales.",
        ),
        (
            "Preventa",
            "Etapa de preventa para inversionistas tempranos, antes de la comercialización masiva.",
        ),
        (
            "Venta",
            "Etapa de venta general al público, con inventario y precios de lista.",
        ),
        (
            "Postventa",
            "Etapa de seguimiento y servicio postventa para clientes existentes.",
        ),
    ]

    for name, description in defaults:
        Stage.objects.get_or_create(
            name=name,
            defaults={"description": description},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("LOTES", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_stages),
    ]

