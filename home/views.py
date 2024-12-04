from django.shortcuts import render
from vehiculos.models import Vehiculo

def inicio(request):
    # Obtener todas las marcas y categorías únicas de los vehículos
    marcas = Vehiculo.objects.values_list('marca', flat=True).distinct()
    categorias = Vehiculo.objects.values_list('categoria', flat=True).distinct()  # Filtramos las categorías únicas
    
    # Obtener los filtros seleccionados
    marca_seleccionada = request.GET.get('marca', '')
    categoria_seleccionada = request.GET.get('categoria', '')
    
    # Filtrar los vehículos según los filtros seleccionados
    vehiculos = Vehiculo.objects.all()
    if marca_seleccionada:
        vehiculos = vehiculos.filter(marca=marca_seleccionada)
    if categoria_seleccionada:
        vehiculos = vehiculos.filter(categoria=categoria_seleccionada)
    
    return render(request, 'home/inicio.html', {
        'vehiculos': vehiculos,
        'marcas': marcas,
        'categorias': categorias,  # Pasa las categorías obtenidas
        'marca_seleccionada': marca_seleccionada,
        'categoria_seleccionada': categoria_seleccionada
    })