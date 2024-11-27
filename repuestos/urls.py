from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.lista_repuestos, name='lista_repuestos'),  # URL de la vista
]