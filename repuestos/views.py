from django.shortcuts import render

def lista_repuestos(request):
    # Aquí puedes añadir lógica para obtener datos de la base de datos si es necesario.
    return render(request, 'repuestos/lista_repuestos.html')  # Renderiza el template