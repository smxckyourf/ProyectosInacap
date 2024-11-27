from django.apps import AppConfig


class TransaccionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transaccion'

from django.apps import AppConfig

class TransaccionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transaccion'

    def ready(self):
        import transaccion.signals  # Reemplaza 'transaccion' con el nombre correcto de tu app