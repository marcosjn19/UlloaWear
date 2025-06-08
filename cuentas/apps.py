# cuentas/apps.py
from django.apps import AppConfig # type: ignore

class CuentasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cuentas'
