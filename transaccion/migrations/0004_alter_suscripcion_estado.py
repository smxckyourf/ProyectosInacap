# Generated by Django 5.0 on 2024-12-05 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaccion', '0003_alter_suscripcion_fecha_termino'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suscripcion',
            name='estado',
            field=models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('ACTIVA', 'Activa'), ('INACTIVA', 'Inactiva'), ('CANCELADA', 'Cancelada')], default='PENDIENTE', max_length=20),
        ),
    ]
