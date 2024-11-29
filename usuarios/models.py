from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Usuario(models.Model):
    # Extendiendo el modelo de User en Django o usando ForeignKey a User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to="profile_pics/", default="default_avatar.png")

    def __str__(self):
        return f"Perfil de {self.user.username}"