# Generated by Django 5.1.2 on 2024-11-07 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repuestos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='repuesto',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
