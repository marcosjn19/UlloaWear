# cuentas/views.py
from django.shortcuts import render, redirect # type: ignore
from django.contrib import messages, auth # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth.tokens import default_token_generator # type: ignore
from django.utils.http import urlsafe_base64_encode # type: ignore
from django.utils.encoding import force_bytes # type: ignore
from django.template.loader import render_to_string # type: ignore
from django.core.mail import send_mail # type: ignore
from django.urls import reverse # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from django.utils.http       import urlsafe_base64_decode # type: ignore
from .forms import FormularioRegistro, FormularioEditarPerfil

# ---------- REGISTRO ----------
def register(request):
    if request.method == "POST":
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["contraseña"])
            user.is_active = False   # inactivo hasta confirmar
            user.save()

            # → genera token + uid
            uid  = urlsafe_base64_encode(force_bytes(user.pk))
            tok  = default_token_generator.make_token(user)
            link = request.build_absolute_uri(
                reverse("activar_cuenta", args=[uid, tok])
            )

            # → renderiza plantilla HTML
            subject = "Activa tu cuenta en UlloaWear"
            body_html = render_to_string("registration/activation_email.html", {
                "user": user, "activation_link": link
            })
            send_mail(
                subject=subject,
                message="",               # dejamos el texto en blanco: usamos html
                from_email=None,          # DEFAULT_FROM_EMAIL
                recipient_list=[user.email],
                html_message=body_html,
            )
            messages.success(request,
                "Te hemos enviado un e-mail para activar tu cuenta.")
            return redirect("iniciar_sesion")
    else:
        form = FormularioRegistro()
    return render(request, "cuentas/registrarse.html", {"form": form})


# ---------- INICIO DE SESIÓN ----------
def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=email, password=password)
        if user:
            auth.login(request, user)
            return redirect("inicio")         # redirige siempre a la portada
        messages.error(request, "Credenciales incorrectas")
    return render(request, "cuentas/login.html")


# ---------- LOGOUT ----------
def logout(request):
    auth.logout(request)
    return redirect("inicio")

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = FormularioEditarPerfil(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('inicio')
    else:
        form = FormularioEditarPerfil(instance=request.user)
    return render(request, "cuentas/editar_perfil.html", {"form": form})

User = get_user_model()

def activar_cuenta(request, uidb64, token):
    try:
        uid  = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (ValueError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "¡Cuenta activada! Ahora puedes iniciar sesión.")
        return redirect("iniciar_sesion")
    else:
        return render(request, "registration/activation_invalid.html")