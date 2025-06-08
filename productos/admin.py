from django.contrib import admin
from .models import Producto, Resena
from django.utils.html import format_html

# Administración para productos
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

class ResenaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'producto', 'user', 'calificacion', 'created_at', 'imagen_miniatura')
    list_filter = ('calificacion', 'created_at')
    search_fields = ('titulo', 'resena', 'producto__nombre', 'user__username')
    readonly_fields = ('imagen_miniatura',)

    def imagen_miniatura(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="100" />', obj.imagen.url)
        return "Sin imagen"
    imagen_miniatura.short_description = "Imagen"

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Resena, ResenaAdmin)