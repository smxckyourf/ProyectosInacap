# usuarios/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'  # Define el namespace para la aplicación 'usuarios'

urlpatterns = [
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('registro/', views.registro, name='registro'),  # Ejemplo de URL para 'perfil'
    path('login/', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    #enlaces para recuperar contraseña
]
