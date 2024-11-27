from django.db import models
from django.contrib.auth.models import User

class Transaccion(models.Model):
    ESTADOS_TRANSACCION = [
        ('AUTHORIZED', 'Autorizada'),
        ('FAILED', 'Fallida'),
        ('CANCELLED', 'Cancelada'),
        ('REVERSED', 'Revertida'),
        ('PENDING', 'Pendiente'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="transacciones")
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS_TRANSACCION, default='PENDING')
    buy_order = models.CharField(max_length=100, unique=True)
    session_id = models.CharField(max_length=100, unique=True)
    token_ws = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    # Datos adicionales de Webpay
    payment_type_code = models.CharField(max_length=50, blank=True, null=True)
    response_code = models.IntegerField(blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    authorization_code = models.CharField(max_length=50, blank=True, null=True)
    card_number = models.CharField(max_length=4, blank=True, null=True)  # Últimos 4 dígitos

    # Información de rastreo y metadata
    ip_cliente = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Transacción {self.buy_order} - {self.get_estado_display()} - ${self.monto}"

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"