# cuentas/forms.py
from django import forms # type: ignore
from .models import Cuenta, PerfilUsuario

# --- 1. clases Tailwind comunes ---
INPUT_TAILWIND = (
    "w-full rounded-xl border border-gray-300 bg-white "
    "py-3 px-4 placeholder-gray-400 "
    "focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
)


class FormularioRegistro(forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput)
    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Cuenta
        fields = ["nombre", "apellido", "telefono", "email", "contraseña"]

    # --- 2. inyección de atributos ---
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "nombre": "Nombre(s)",
            "apellido": "Apellidos",
            "telefono": "10 dígitos",
            "email": "usuario@correo.com",
            "contraseña": "••••••••",
            "confirmar_contraseña": "Repite la contraseña",
        }

        for name, field in self.fields.items():
            # placeholder personalizado
            if name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[name]
            # clases Tailwind
            field.widget.attrs["class"] = INPUT_TAILWIND

    # --- 3. validación de contraseñas ---
    def clean(self):
        cleaned = super().clean()
        if cleaned.get("contraseña") != cleaned.get("confirmar_contraseña"):
            raise forms.ValidationError("¡Las contraseñas no coinciden!")


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
