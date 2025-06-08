# cuentas/pipelines.py

from django.utils.crypto import get_random_string

def populate_required_fields(backend, details, response, *args, **kwargs):
    """
    Rellena los campos obligatorios antes de crear el Usuario:
      - usuario  ← details['username']
      - nombre   ← details['fullname']
      - apellido ← resto tras primer espacio de fullname
      - email    ← details['email']
    """
    user = kwargs.get("user")
    if user:
        return  # ya existe, es un login

    # 1️⃣ Usuario: tu alias siempre está en details['username']
    username = details.get("username") or f"user_{get_random_string(6)}"

    # 2️⃣ Fullname: en Discord viene aquí tu Display Name
    fullname = details.get("fullname") or username
    first, *rest = fullname.split(" ", 1)
    last = rest[0] if rest else ""

    # 3️⃣ Email (si no viene, inventamos uno local)
    email = details.get("email") or f"{username}@{backend.name}.local"

    return {
        "usuario":  username,
        "nombre":   first,
        "apellido": last,
        "email":    email,
    }


def activate_user(backend, user=None, *args, **kwargs):
    """
    Tras crear el usuario lo marcamos activo para que inicie sesión.
    """
    if user and not user.is_active:
        user.is_active = True
        user.save()