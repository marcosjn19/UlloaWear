# cuentas/admin.py
from django.contrib import admin # type: ignore
from django.contrib.auth.admin import UserAdmin # type: ignore
from .models import Cuenta, PerfilUsuario
from django.utils.html import format_html # type: ignore

# Register your models here.
class CuentasAdmin(UserAdmin):
    list_display = ('email', 'nombre', 'apellido', 'usuario', 'ultimo_acceso', 'fecha_registro', 'is_active')
    list_display_links = ('email', 'nombre', 'apellido')
    readonly_fields = ('ultimo_acceso', 'fecha_registro')
    ordering = ('fecha_registro',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class PerfilUsuarioAdmin(admin.ModelAdmin):
    def miniatura(self, objeto):
        if objeto.foto_perfil:
            return format_html('<img src="{}" width="30" style="border-radius:50%;">', objeto.foto_perfil.url)
        return "-"
    
    miniatura.short_description = 'Foto de perfil'
    list_display = ('miniatura', 'usuario', 'ciudad', 'estado', 'pais')

# Registro en el panel de administración

admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)
admin.site.register(Cuenta, CuentasAdmin)