from django.db import models
from django.contrib.auth.models import User
from vehiculos.models import Vehiculo  # Importa el modelo del auto si está en otra app

class Reserva(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('Completada', 'Completada')])
    transaccion_id = models.CharField(max_length=100, blank=True, null=True)  # Para almacenar el token de Webpay
    monto = models.DecimalField(max_digits=10, decimal_places=2)  # Monto de la transacción

    def __str__(self):
        return f"Reserva de {self.vehiculo} por {self.usuario}"