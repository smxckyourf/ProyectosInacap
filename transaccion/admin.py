from django.contrib import admin
from transaccion.models import Ingresos
# Register your models here.
@admin.register(Ingresos)
class IngresosAdmin(admin.ModelAdmin):
    list_display = ('transaccion', 'monto', 'fecha_ingreso')
    search_fields = ('transaccion__buy_order',)
    list_filter = ('fecha_ingreso',)