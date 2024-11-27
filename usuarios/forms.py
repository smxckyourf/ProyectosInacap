# usuarios/forms.py
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
from .models import Usuario
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo")
    rut = forms.CharField(
        required=True,
        max_length=12,
        validators=[
            RegexValidator(
                regex=r"^\d{1,2}\.\d{3}\.\d{3}-[0-9kK]$",
                message="El RUT debe estar en el formato 12.345.678-9",
            )
        ],
        help_text="Formato: 12.345.678-9"
    )
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Tipo de Usuario")

    class Meta:
        model = User
        fields = [ "first_name", "last_name", "rut", "email", "password1", "password2", "grupo"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]  # Usa el email como username
        if commit:
            user.save()
        # Guarda el campo rut en el perfil de usuario
            Usuario.objects.create(user=user, rut=self.cleaned_data["rut"])
        return user