from django.urls import path
from . import views

app_name = 'vehiculos'
urlpatterns = [
    path('<int:id>/', views.detalle_vehiculo, name='detail'),  # Ruta existente
    path('', views.vehiculo_list, name='list'),  # Lista de vehículos
    path('create/', views.vehiculo_create, name='create'),  # Crear vehículo
    path('<int:pk>/update/', views.vehiculo_update, name='update'),  # Actualizar vehículo
    path('<int:pk>/delete/', views.vehiculo_delete, name='delete'),  # Eliminar vehículo
]
