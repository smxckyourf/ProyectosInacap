from django.db.models.signals import post_save
from django.dispatch import receiver
from transaccion.models import Transaccion
from ventas.models import Compra

@receiver(post_save, sender=Transaccion)
def registrar_compra(sender, instance, created, **kwargs):
    # Validar si la transacción tiene un estado que permite generar una compra
    if instance.estado == 'AUTHORIZED':  # Cambia esto según tus requerimientos
        # Verificar si ya existe una compra asociada a esta transacción
        if not Compra.objects.filter(transaccion=instance).exists():
            # Crear la compra
            Compra.objects.create(
                vehiculo=instance.vehiculo,
                usuario=instance.usuario,
                transaccion=instance,
                monto_total=instance.monto
            )