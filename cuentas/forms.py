# cuentas/forms.py
from django import forms # type: ignore
from django.contrib.auth.forms import SetPasswordForm # type: ignore
from .models import Cuenta, PerfilUsuario

# --- 1. clases Tailwind comunes ---
INPUT_TAILWIND = (
    "w-full rounded-xl border border-gray-300 bg-white "
    "py-3 px-4 placeholder-gray-400 "
    "focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
)


class FormularioRegistro(forms.ModelForm):
    usuario = forms.CharField(
        max_length=50,
        widget=forms.TextInput
    )
    contraseña = forms.CharField(
        widget=forms.PasswordInput
    )
    confirmar_contraseña = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = Cuenta
        fields = ["nombre", "apellido", "telefono", "email", "usuario", "contraseña"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "nombre": "Nombre(s)",
            "apellido": "Apellidos",
            "telefono": "10 dígitos",
            "email": "usuario@correo.com",
            "usuario": "Elige un nombre de usuario",
            "contraseña": "••••••••",
            "confirmar_contraseña": "Repite la contraseña",
        }

        for name, field in self.fields.items():
            # placeholder personalizado
            if name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[name]
            # clases Tailwind
            field.widget.attrs["class"] = INPUT_TAILWIND

    def clean_usuario(self):
        usuario = self.cleaned_data.get("usuario", "").strip()
        if Cuenta.objects.filter(usuario__iexact=usuario).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return usuario

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("contraseña")
        pwd2 = cleaned.get("confirmar_contraseña")
        if pwd and pwd2 and pwd != pwd2:
            raise forms.ValidationError("¡Las contraseñas no coinciden!")
        return cleaned


class FormularioUsuario(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ('nombre', 'apellido', 'telefono')

    def __init__(self, *args, **kwargs):
        super(FormularioUsuario, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class FormularioPerfilUsuario(forms.ModelForm):
    foto_perfil = forms.ImageField(
        required=False,
        error_messages={'invalid': 'Solo se permiten archivos de imagen.'},
        widget=forms.FileInput
    )

    class Meta:
        model = PerfilUsuario
        fields = ('direccion_1', 'direccion_2', 'ciudad', 'estado', 'pais', 'foto_perfil')

    def __init__(self, *args, **kwargs):
        super(FormularioPerfilUsuario, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
class FormularioEditarPerfil(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ('nombre', 'apellido')

    def __init__(self, *args, **kwargs):
        super(FormularioEditarPerfil, self).__init__(*args, **kwargs)
        # Aplica estilos Tailwind a cada campo
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            })
            
class FormularioCambioContraseña(SetPasswordForm):
    """
    Este formulario se usará en PasswordResetConfirmView 
    para añadir clases Tailwind a los inputs.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Actualiza attrs de cada campo
        for field_name in ("new_password1", "new_password2"):
            field = self.fields[field_name]
            field.widget.attrs.update({
                "class": INPUT_TAILWIND,
                "placeholder": "••••••••",
                "autocomplete": "new-password",
            })
