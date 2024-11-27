from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Transaccion, Compra

def registrar_compra(transaccion_id, usuario, vehiculo_id, monto_total):
    # Obtén la transacción y verifica que exista
    transaccion = get_object_or_404(Transaccion, id=transaccion_id)
    
    # Crea una nueva compra basada en la transacción
    compra = Compra.objects.create(
        vehiculo_id=vehiculo_id,  # Asegúrate de que `vehiculo_id` esté disponible
        usuario=usuario,  # Usuario que realiza la compra
        transaccion=transaccion,  # Relación con la transacción
        monto_total=monto_total  # Monto de la compra
    )
    return compra