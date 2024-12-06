from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Vehiculo(models.Model):
    propietario = models.ForeignKey(User, on_delete=models.CASCADE,  blank=True)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    año = models.IntegerField()
    precio = models.IntegerField()
    kilometraje = models.IntegerField()
    color = models.CharField(max_length=30)
    descripcion = models.TextField()
    disponibilidad = models.BooleanField(default=True)
    categoria = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.año})"
    
    @property
    def disponibilidad_texto(self):
        return "Si" if self.disponibilidad else "No"
    
class ImagenVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='images/vehiculos/', blank=True, null=True)

    def __str__(self):
        return f"Imagen de {self.vehiculo.marca} {self.vehiculo.modelo}"


class CaracteristicaVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name="caracteristicas")
    nombre = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre}: {self.valor} - {self.vehiculo}"