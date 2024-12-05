from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required
from transaccion.models import Suscripcion


def perfil_usuario(request):
    # Filtrar la suscripción activa más reciente del usuario
    suscripcion = Suscripcion.objects.filter(propietario=request.user, estado="ACTIVA").order_by('-fecha_inicio').first()

    # Determinar el plan, la fecha de término y el límite de inventario
    if suscripcion:
        if suscripcion.monto == 10000:
            plan = "Plan Básico"
            limite_inventario = 50  # Límite para el plan básico
        elif suscripcion.monto == 20000:
            plan = "Plan Intermedio"
            limite_inventario = 200  # Límite para el plan intermedio
        elif suscripcion.monto == 30000:
            plan = "Plan Avanzado"
            limite_inventario = float('inf')  # Límite ilimitado para el plan avanzado
        else:
            plan = "Plan Desconocido"
            limite_inventario = 0  # Sin límite válido

        fecha_termino = suscripcion.fecha_termino
    else:
        plan = "Sin plan"
        fecha_termino = None
        limite_inventario = "No tiene una suscripción activa"

    return render(request, 'usuarios/perfil.html', {
        'plan': plan,
        'fecha_termino': fecha_termino,
        'limite_inventario': limite_inventario
    })

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

