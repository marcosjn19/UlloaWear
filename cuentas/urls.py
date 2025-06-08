# cuentas/urls.py
from django.urls import path # type: ignore
from django.contrib.auth import views as auth_views # type: ignore
from .forms import FormularioCambioContraseña
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
    
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', subject_template_name='registration/password_reset_subject.txt', email_template_name='registration/password_reset_email.txt', html_email_template_name='registration/password_reset_email.html', success_url='done/'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html', form_class=FormularioCambioContraseña, success_url='/reset/done/',), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]