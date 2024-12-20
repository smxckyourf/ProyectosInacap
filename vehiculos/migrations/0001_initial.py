# Generated by Django 5.0 on 2024-12-04 02:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('año', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('kilometraje', models.IntegerField()),
                ('color', models.CharField(max_length=30)),
                ('descripcion', models.TextField()),
                ('disponibilidad', models.BooleanField(default=True)),
                ('categoria', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImagenVehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='images/vehiculos/')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='vehiculos.vehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='CaracteristicaVehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('valor', models.CharField(max_length=50)),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caracteristicas', to='vehiculos.vehiculo')),
            ],
        ),
    ]
