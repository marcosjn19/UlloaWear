from django.contrib import admin
from .models import Producto

# Administración para productos
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


admin.site.register(Producto, ProductoAdmin)
