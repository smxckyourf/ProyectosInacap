from django import forms
from .models import Vehiculo, ImagenVehiculo
from django.forms import modelformset_factory

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = '__all__'  # o especifica los campos: ['marca', 'modelo', 'año', etc.]

    # Validación personalizada para el campo 'marca'
    def clean_marca(self):
        marca = self.cleaned_data.get('marca')
        if not marca:
            raise forms.ValidationError("La marca es obligatoria.")
        if len(marca) > 50:
            raise forms.ValidationError("La marca no puede tener más de 50 caracteres.")
        return marca

    # Validación personalizada para el campo 'modelo'
    def clean_modelo(self):
        modelo = self.cleaned_data.get('modelo')
        if not modelo:
            raise forms.ValidationError("El modelo es obligatorio.")
        if len(modelo) > 50:
            raise forms.ValidationError("El modelo no puede tener más de 50 caracteres.")
        return modelo

    # Validación personalizada para el campo 'año'
    def clean_año(self):
        año = self.cleaned_data.get('año')
        if año < 1886:  # Año del primer automóvil
            raise forms.ValidationError("El año no puede ser anterior a 1886.")
        elif año > 2025:  # Límite razonable superior
            raise forms.ValidationError("El año no puede ser mayor a 2025.")
        return año

    # Validación personalizada para el campo 'precio'
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser un valor positivo.")
        return precio

    # Validación personalizada para el campo 'kilometraje'
    def clean_kilometraje(self):
        kilometraje = self.cleaned_data.get('kilometraje')
        if kilometraje < 0:
            raise forms.ValidationError("El kilometraje no puede ser negativo.")
        return kilometraje

    # Validación personalizada para el campo 'color'
    def clean_color(self):
        color = self.cleaned_data.get('color')
        if len(color) > 30:
            raise forms.ValidationError("El color no puede tener más de 30 caracteres.")
        return color

    # Validación personalizada para el campo 'disponibilidad'
    def clean_disponibilidad(self):
        disponibilidad = self.cleaned_data.get('disponibilidad')
        if disponibilidad not in [True, False]:
            raise forms.ValidationError("La disponibilidad debe ser 'True' o 'False'.")
        return disponibilidad

class ImagenVehiculoForm(forms.ModelForm):
    class Meta:
        model = ImagenVehiculo
        fields = ['imagen']

ImagenVehiculoFormSet = modelformset_factory(ImagenVehiculo, form=ImagenVehiculoForm, extra=5)