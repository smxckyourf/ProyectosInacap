"""
URL configuration for Automotora project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# automotora/urls.py (archivo principal del proyecto)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),          
    path('vehiculos/', include('vehiculos.urls')),       # URL de inicio # URLs de 'vehiculos'  # URLs de 'reservas'     # URLs de 'compras'
    path('usuarios/', include('usuarios.urls')),    # URLs de 'usuarios'
    path('repuestos/', include('repuestos.urls')),
    path('', include('transaccion.urls')),
]    

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)