from django.contrib import admin
from .models import Categoria

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'padre')  # muestra la jerarquía en tabla
    list_filter = ('padre',)  # filtrar por categoría padre
    search_fields = ('nombre',)
    ordering = ('padre__nombre', 'nombre')  # ordena por jerarquía

admin.site.register(Categoria, CategoriaAdmin)
