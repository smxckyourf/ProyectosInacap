# Generated by Django 5.0 on 2024-11-27 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculos', '0004_remove_vehiculo_imagen_imagenvehiculo'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculo',
            name='categoria',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]