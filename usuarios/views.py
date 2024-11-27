from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required

def perfil_usuario(request):
    # Aquí puedes agregar la lógica para mostrar el perfil del usuario
    return render(request, 'usuarios/perfil.html')

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Guardar el usuario sin confirmar aún para añadir un username automático
            user = form.save(commit=False)
            
            # Generar un username automático basado en el email
            user.username = form.cleaned_data["email"]  # Usa el correo como username
            
            # Guardar el usuario con el username generado
            user.save()
            
            # Asignar el grupo seleccionado al usuario
            grupo = form.cleaned_data.get('grupo')
            user.groups.add(grupo)
            
            # Iniciar sesión automáticamente después de registrarse (opcional)
            login(request, user)
            
            # Redirige a la página de inicio o a la página deseada
            return redirect('home:inicio')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html', {'user': request.user})