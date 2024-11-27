from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from django.conf import settings
import logging
from transbank.common.options import WebpayOptions
import random
from vehiculos.models import Vehiculo
from reserva_vehiculo.models import Reserva
from transaccion.models import Transaccion
import uuid


logger = logging.getLogger(__name__)

@login_required
def iniciar_pago(request, vehiculo_id):
    vehiculo = Vehiculo.objects.get(id=vehiculo_id)
    amount = vehiculo.precio  # Usar el precio del auto como monto

    # Crear una instancia de reserva con estado 'Pendiente'
    reserva = Reserva.objects.create(
        vehiculo=vehiculo,
        usuario=request.user,
        estado='Pendiente',
        monto=amount
    )

    options = WebpayOptions(
        commerce_code=settings.TRANSBANK_CC,
        api_key=settings.TRANSBANK_API_KEY,
        integration_type=IntegrationType.TEST
    )
    tx = Transaction(options)

    buy_order = f"orden_{reserva.id}"  # Usar el ID de la reserva para referencia
    session_id = str(uuid.uuid4())
    return_url = request.build_absolute_uri('/webpay-confirmacion/')

    try:
        response = tx.create(buy_order, session_id, amount, return_url)
        redirect_url = response['url']
        token = response['token']

        # Guarda el token en la reserva para seguimiento
        reserva.transaccion_id = token
        reserva.save()

        return redirect(f"{redirect_url}?token_ws={token}")

    except Exception as e:
        return render(request, 'transaccion/error.html', {'error': str(e)})
    

def confirmacion_pago(request):
    token = request.GET.get('token_ws')

    # Configuración de opciones de Webpay
    options = WebpayOptions(
        commerce_code=settings.TRANSBANK_CC,
        api_key=settings.TRANSBANK_API_KEY,
        integration_type=IntegrationType.TEST
    )
    tx = Transaction(options=options)

    # Ejecuta la función commit de Webpay
    response = tx.commit(token=token)
    print(f"Respuesta de commit: {response}")  # Muestra la respuesta de la transacción para verificar

    # Intenta asociar la reserva con este token
    try:
        reserva = Reserva.objects.get(transaccion_id=token)
        
        # Si la transacción fue autorizada
        if response['status'] == 'AUTHORIZED':
            # Guarda la transacción en la base de datos
            Transaccion.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                monto=response['amount'],
                estado=response['status'],
                buy_order=response['buy_order'],
                session_id=response['session_id'],
                token_ws=token,
                payment_type_code=response.get('payment_type_code'),
                response_code=response.get('response_code'),
                transaction_date=response.get('transaction_date'),
                authorization_code=response.get('authorization_code'),
                card_number=response.get('card_detail', {}).get('card_number'),
                ip_cliente=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
            
            # Actualiza el estado de la reserva
            reserva.estado = 'Completada'
            reserva.save()
            return render(request, 'pago_exitoso.html', {'response': response, 'reserva': reserva})
        else:
            reserva.estado = 'Pendiente'
            reserva.save()
            return render(request, 'pago_fallido.html', {'response': response, 'reserva': reserva})
    
    except Reserva.DoesNotExist:
        # Si no se encuentra la reserva, muestra un error
        return render(request, 'transaccion/error.html', {'error': 'Reserva no encontrada.'})



def estado_transaccion(request, token):
    # Configurar los parámetros de Webpay en modo de integración
    options = WebpayOptions(
        commerce_code=settings.TRANSBANK_CC,
        api_key=settings.TRANSBANK_API_KEY,
        integration_type=IntegrationType.TEST
    )
    
    # Crear una instancia de Transaction con las opciones configuradas
    tx = Transaction(options)
    

        # Obtener el estado de la transacción usando el token
    response = tx.status(token)
        
        # Enviar los datos a la plantilla para mostrarlos
    return render(request, 'estado_transaccion.html', {'response': response})
    

def cancelar_pago(request):
    # Si es necesario, puedes capturar datos relevantes de la transacción que se cancela
    return render(request, 'transaccion_cancelada.html')