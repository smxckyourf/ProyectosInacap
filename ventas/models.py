from django.db import models
from vehiculos.models import Vehiculo
from django.contrib.auth.models import User
from transaccion.models import Transaccion  # Asegúrate de importar el modelo correctamente

class Compra(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    transaccion = models.ForeignKey(Transaccion, on_delete=models.CASCADE, blank=True, null=True, related_name="compras")  # Asociar con Transacción
    fecha_compra = models.DateTimeField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra de {self.usuario} - {self.vehiculo} por ${self.monto_total}"

