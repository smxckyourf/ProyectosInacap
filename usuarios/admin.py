from django.contrib import admin
from django import forms
from .forms import UserCreationForm
from usuarios.models import Usuario
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
# Register your models here.
admin.site.register(Usuario)

class UserCreationForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Grupo")

    class Meta:
        model = User
        fields = ("username", "password", "group")

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.groups.add(self.cleaned_data["group"])  # Asigna el grupo seleccionado al usuario
        return user
    
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm  # Usa el formulario personalizado en el panel de administración
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'group'),  # Incluye el campo "group"
        }),
    )

# Desregistra el modelo `User` por defecto y registra el personalizado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)