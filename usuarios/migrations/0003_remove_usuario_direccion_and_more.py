# Generated by Django 5.1.2 on 2024-11-07 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuario_direccion_usuario_fecha_nacimiento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='fecha_nacimiento',
        ),
    ]
