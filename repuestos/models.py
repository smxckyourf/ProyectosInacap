from django.db import models

# Create your models here.
class Repuesto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    compatibilidad = models.CharField(max_length=100)  # Compatible con modelos específicos
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} (Compatible: {self.compatibilidad})"