from django.db import migrations


def fix_stages(apps, schema_editor):
    Stage = apps.get_model("LOTES", "Stage")

    rename_map = {
        "Venta": "Construcción",
        "Postventa": "Entrega",
    }

    for old_name, new_name in rename_map.items():
        for stage in Stage.objects.filter(name=old_name):
            stage.name = new_name
            stage.save()

    descriptions = {
        "Lanzamiento": "Etapa inicial del proyecto con lanzamiento comercial y difusión a inversionistas.",
        "Preventa": "Oferta especial para inversionistas tempranos antes de la venta abierta al público.",
        "Construcción": "Fase de construcción, urbanismo y adecuación de servicios del proyecto.",
        "Entrega": "Etapa de entrega de lotes y acompañamiento postventa a los compradores.",
    }

    for name, desc in descriptions.items():
        stage, created = Stage.objects.get_or_create(name=name, defaults={"description": desc})
        if not created:
            Stage.objects.filter(pk=stage.pk).update(description=desc)


class Migration(migrations.Migration):
    dependencies = [
        ("LOTES", "0004_lotimage_gallery"),
    ]

    operations = [
        migrations.RunPython(fix_stages, migrations.RunPython.noop),
    ]

