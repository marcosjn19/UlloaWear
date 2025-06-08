# cuentas/views.py
from django.shortcuts import render, redirect # type: ignore
from django.contrib import messages, auth # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from .forms import FormularioRegistro, FormularioEditarPerfil

# ---------- REGISTRO ----------
def register(request):
    if request.method == "POST":
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data["contraseña"])
            usuario.is_active = True          # sin validación por correo
            usuario.save()
            messages.success(request, "Cuenta creada. Ahora inicia sesión.")
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