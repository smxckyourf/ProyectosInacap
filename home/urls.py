# home/urls.py
from django.urls import path
from . import views

app_name = 'home'  # Define el namespace para esta aplicación

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Define la URL de inicio con el nombre 'inicio'
]
