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
from .models import Ingresos
from django.db.models import Sum
from calendar import month_name
from django.utils.timezone import now
from django.contrib import messages
from .models import Suscripcion, PagoSuscripcion
from django.shortcuts import render, get_object_or_404
from dateutil.relativedelta import relativedelta




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
        print(f"Redirigiendo a: {redirect_url}?token_ws={token}")  # Agrega esto para depurar
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
            reserva.estado = 'Fallida'
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

def obtener_meses():
    nombres_meses = [
        {'numero': i, 'nombre': nombre} 
        for i, nombre in enumerate(
            ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'], 
            start=1
        )
    ]
    return nombres_meses   
@login_required
def vista_total_ingresos(request):
    # Obtener los parámetros del filtro desde el GET
    month = request.GET.get('month')
    year = request.GET.get('year')

    # Validar el año
    current_year = now().year
    if year and int(year) > current_year:
        messages.error(request, "El año no puede ser mayor al actual.")
        return render(request, 'ingresos_totales.html', {
            'total_ingresos': 0,
            'month': month,
            'year': year,
            'meses': obtener_meses()  # Pasa los meses en español
        })

    # Obtener todos los ingresos
    ingresos = Ingresos.objects.all()

    # Filtrar por mes y/o año si se seleccionaron
    if month:
        ingresos = ingresos.filter(fecha_ingreso__month=month)
    if year:
        ingresos = ingresos.filter(fecha_ingreso__year=year)

    # Calcular el total de ingresos
    total_ingresos = ingresos.aggregate(total=Sum('monto'))['total'] or 0

    # Pasar los valores al template
    return render(request, 'ingresos_totales.html', {
        'total_ingresos': total_ingresos,
        'month': month,
        'year': year,
        'meses': obtener_meses()  # Pasa los meses en español
    })



##### VISTAS PARA LA SUSCRIPCIÓN

def iniciar_suscripcion(request):
    if request.method == 'POST':

        suscripcion_existente = Suscripcion.objects.filter(propietario=request.user, estado='ACTIVA').first()
        if suscripcion_existente:
            return render(request, 'suscripcion/suscripcionlista.html', {'error': 'Ya tienes una suscripción activa.'})
        # Captura el plan seleccionado desde el formulario
        plan = request.POST.get('plan')

        # Verifica que se haya seleccionado un plan
        if not plan:
            return render(request, 'suscripcion/escogeplan.html', {
                'error': 'Por favor, selecciona un plan antes de continuar.'
            })


        # Lógica para determinar el monto según el plan seleccionado
        if plan == 'plan_basico':
            monto = 10000
        elif plan == 'plan_intermedio':
            monto = 20000
        elif plan == 'plan_avanzado':
            monto = 30000
        else:
            return render(request, 'suscripcion/planinvalido.html', {
                'error': 'Plan no válido.'
            })

        # Crear la suscripción con estado "Pendiente"
        suscripcion = Suscripcion.objects.create(
            propietario=request.user,
            monto=monto,
            estado='PENDIENTE',
            fecha_termino=None  # Fecha de término se establece tras el pago
        )

        # Configuración de Webpay
        options = WebpayOptions(
            commerce_code=settings.TRANSBANK_CC,
            api_key=settings.TRANSBANK_API_KEY,
            integration_type=IntegrationType.TEST  # Usar TEST para pruebas
        )
        tx = Transaction(options)

        # Configuración de la transacción
        buy_order = f"subs_{suscripcion.id}"
        session_id = str(uuid.uuid4())
        return_url = request.build_absolute_uri(f'/confirmacion-suscripcion/{suscripcion.id}/')

        try:
            # Crear la transacción con Webpay
            response = tx.create(buy_order, session_id, monto, return_url)
            redirect_url = response['url']
            token = response['token']

            # Asocia el token de Webpay a la suscripción
            suscripcion.transaccion_id = token
            suscripcion.save()

            # Redirige al usuario a Webpay
            return redirect(f"{redirect_url}?token_ws={token}")

        except Exception as e:
            return render(request, 'suscripcion/opciones.html', {
                'warning': f"Error al conectar con Webpay: {str(e)}"
            })

    # Renderiza el formulario inicial
    return render(request, 'suscripcion/opciones.html')

def confirmacion_suscripcion(request, suscripcion_id):
    # Obtén la suscripción
    suscripcion = get_object_or_404(Suscripcion, id=suscripcion_id)

    # Obtén el token de Webpay
    token_ws = request.GET.get('token_ws')

    # Verifica el estado del pago con Webpay
    options = WebpayOptions(
        commerce_code=settings.TRANSBANK_CC,
        api_key=settings.TRANSBANK_API_KEY,
        integration_type=IntegrationType.TEST
    )
    tx = Transaction(options)

    try:
        # Verifica el estado de la transacción con Webpay
        response = tx.commit(token_ws)

        if response['status'] == 'AUTHORIZED':  # Pago autorizado
            # Actualiza el estado de la suscripción a "Activa"
            suscripcion.estado = 'ACTIVA'
            suscripcion.fecha_termino = suscripcion.fecha_inicio + relativedelta(months=1)
            suscripcion.save()

            # Registra el pago como "Pagado"
            pago = PagoSuscripcion.objects.create(
                suscripcion=suscripcion,
                monto=suscripcion.monto,
                estado='PAGADO'
            )
        else:
            # Si el pago falla, deja la suscripción como "Pendiente" o "Inactiva"
            suscripcion.estado = 'INACTIVA'
            suscripcion.save()
            pago = None

        return render(request, 'suscripcion/confirmacion.html', {
            'suscripcion': suscripcion,
            'pago': pago,
            'response': response
        })

    except Exception as e:
        return render(request, 'suscripcion/error.html', {
            'error': f"Error al procesar la transacción: {str(e)}"
        })
    

@login_required
def vista_total_ingresos_adm(request):
    # Obtener los parámetros del filtro desde el GET
    month = request.GET.get('month')
    year = request.GET.get('year')

    # Validar el año
    current_year = now().year
    if year and int(year) > current_year:
        messages.error(request, "El año no puede ser mayor al actual.")
        return render(request, 'ingresos_mensuales.html', {
            'total_ingresos': 0,
            'month': month,
            'year': year,
            'meses': obtener_meses()  # Pasa los meses en español
        })

    # Obtener todos los ingresos
    pagos = PagoSuscripcion.objects.all()

    # Filtrar por mes y/o año si se seleccionaron
    if month:
        pagos = pagos.filter(fecha_pago__month=month)
    if year:
        pagos = pagos.filter(fecha_pago__year=year)

    # Calcular el total de ingresos
    total_ingresos = pagos.aggregate(total=Sum('monto'))['total'] or 0

    # Pasar los valores al template
    return render(request, 'suscripcion/ingresos_mensuales.html', {
        'total_ingresos': total_ingresos,
        'month': month,
        'year': year,
        'meses': obtener_meses()  # Pasa los meses en español
    })