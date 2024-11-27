from django.shortcuts import render
from vehiculos.models import Vehiculo

def inicio(request):
    vehiculos = Vehiculo.objects.all()  # Consulta de todos los vehículos
    return render(request, 'home/inicio.html', {'vehiculos': vehiculos})