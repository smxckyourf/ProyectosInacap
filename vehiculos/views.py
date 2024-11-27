# vehiculos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehiculo, ImagenVehiculo
from .forms import VehiculoForm, ImagenVehiculoFormSet  # Asegúrate de tener un formulario para el modelo
from .utils import group_required

def detalle_vehiculo(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    return render(request, 'vehiculos/detalle.html', {'vehiculo': vehiculo})

# Crear un vehículo
@group_required('propietario', 'administrador')
def vehiculo_create(request):
    if request.method == 'POST':
        # Crea instancias del formulario de Vehículo y el formset de imágenes con los datos POST
        form = VehiculoForm(request.POST)
        imagen_formset = ImagenVehiculoFormSet(request.POST, request.FILES, queryset=ImagenVehiculo.objects.none())
        
        if form.is_valid() and imagen_formset.is_valid():
            # Guarda el vehículo
            vehiculo = form.save()
            
            # Guarda cada imagen asociada al vehículo
            for imagen_form in imagen_formset.cleaned_data:
                if imagen_form:
                    ImagenVehiculo.objects.create(vehiculo=vehiculo, imagen=imagen_form['imagen'])

            return redirect('vehiculos:list')  # Redirige a la lista de vehículos o a la página deseada

    else:
        # Inicializa los formularios vacíos en GET
        form = VehiculoForm()
        imagen_formset = ImagenVehiculoFormSet(queryset=ImagenVehiculo.objects.none())

    return render(request, 'vehiculos/vehiculo_form.html', {
        'form': form,
        'imagen_formset': imagen_formset
    })

# Leer los vehículos (lista)
@group_required('propietario', 'administrador')
def vehiculo_list(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculos/vehiculo_list.html', {'vehiculos': vehiculos})

# Detalle de un vehículo
@group_required('propietario', 'administrador')
def vehiculo_detail(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    return render(request, 'vehiculos/vehiculo_detail.html', {'vehiculo': vehiculo})

# Actualizar un vehículo
@group_required('propietario', 'administrador')
def vehiculo_update(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == 'POST':
        # Crear instancias del formulario de Vehículo y el formset de imágenes con los datos POST
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo)
        imagen_formset = ImagenVehiculoFormSet(request.POST, request.FILES, queryset=vehiculo.imagenes.all())

        if form.is_valid() and imagen_formset.is_valid():
            # Guardar el vehículo
            vehiculo = form.save()

            # Guardar cada imagen en el formset
            for imagen_form in imagen_formset:
                if imagen_form.cleaned_data:
                    imagen = imagen_form.save(commit=False)
                    imagen.vehiculo = vehiculo
                    imagen.save()

            return redirect('vehiculos:list')  # Redirige a la lista de vehículos después de guardar

    else:
        # Inicializar los formularios y formset en GET
        form = VehiculoForm(instance=vehiculo)
        imagen_formset = ImagenVehiculoFormSet(queryset=vehiculo.imagenes.all())

    return render(request, 'vehiculos/vehiculo_form.html', {
        'form': form,
        'imagen_formset': imagen_formset
    })

# Eliminar un vehículo
@group_required('propietario', 'administrador')
def vehiculo_delete(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo.delete()
        return redirect('vehiculos:list')
    return render(request, 'vehiculos/vehiculo_confirm_delete.html', {'vehiculo': vehiculo})