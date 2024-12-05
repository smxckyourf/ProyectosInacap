from django.shortcuts import render
from vehiculos.models import Vehiculo

def inicio(request):
    # Obtener todos los vehículos de la base de datos
    vehiculos = Vehiculo.objects.all()

    # Obtener todas las marcas y categorías únicas de los vehículos
    marcas = vehiculos.values_list('marca', flat=True).distinct()
    categorias = vehiculos.values_list('categoria', flat=True).distinct()

    # Obtener los filtros seleccionados
    marca_seleccionada = request.GET.get('marca', '')  # Obtener el filtro por marca
    categoria_seleccionada = request.GET.get('categoria', '')  # Obtener el filtro por categoría

    # Filtrar los vehículos según los filtros seleccionados
    if marca_seleccionada:
        vehiculos = vehiculos.filter(marca=marca_seleccionada)
    if categoria_seleccionada:
        vehiculos = vehiculos.filter(categoria=categoria_seleccionada)

    # Renderizar la plantilla con los datos
    return render(request, 'home/inicio.html', {
        'vehiculos': vehiculos,
        'marcas': marcas,
        'categorias': categorias,
        'marca_seleccionada': marca_seleccionada,
        'categoria_seleccionada': categoria_seleccionada,
    })