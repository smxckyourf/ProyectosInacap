# urls.py
from django.urls import path
from . import views

app_name = 'transaccion'
urlpatterns = [
    path('iniciar-pago/<int:vehiculo_id>/', views.iniciar_pago, name='iniciar_pago'),
    path('webpay-confirmacion/', views.confirmacion_pago, name='confirmacion_pago'),
    path('transaccion/estado/<str:token>/', views.estado_transaccion, name='estado_transaccion'),
    path('cancelar-pago/', views.cancelar_pago, name='cancelar_pago'),
    path('ingresos-totales/', views.vista_total_ingresos, name='vista_total_ingresos'),
    path('ingresos-totales-adm/', views.vista_total_ingresos_adm, name='vista_total_ingresos_adm'),
    path('iniciar-suscripcion/', views.iniciar_suscripcion, name='iniciar_suscripcion'),
    path('confirmacion-suscripcion/<int:suscripcion_id>/', views.confirmacion_suscripcion, name='confirmacion_suscripcion'),
]