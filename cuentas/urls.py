# cuentas/urls.py
from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('registrarse/', views.register, name='registrarse'),
    path('iniciar-sesion/', views.login, name='iniciar_sesion'),
    path('cerrar-sesion/', views.logout, name='cerrar_sesion'),
    
    # path('recuperar-contrasena/', views.forgotPassword, name='recuperar_contrasena'),
    # path('restablecer-contrasena/', views.resetPassword, name='restablecer_contrasena'),
    # path('validar-restablecimiento/<uidb64>/<token>/', views.resetpassword_validate, name='validar_restablecimiento'),
    # path('activar-cuenta/<uidb64>/<token>/', views.activate, name='activar_cuenta'),

    # path('mis-ordenes/', views.my_orders, name='mis_ordenes'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
]