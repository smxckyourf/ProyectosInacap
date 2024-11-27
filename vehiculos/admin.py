
# Register your models here.
# vehiculos/admin.py
from django.contrib import admin
from .models import Vehiculo

# Registrar el modelo en el administrador
admin.site.register(Vehiculo)
