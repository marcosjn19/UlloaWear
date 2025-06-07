from django import forms
from models import Cuenta, PerfilUsuario

class FormularioRegistro(forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese contraseña',
        'class': 'form-control',
    }))

    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirme contraseña',
        'class': 'form-control',
    }))

    class Meta:
        model = Cuenta
        fields = ['nombre', 'apellido', 'telefono', 'email', 'contraseña']

    def __init__(self, *args, **kwargs):
        super(FormularioRegistro, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['placeholder'] = 'Ingrese su nombre'
        self.fields['apellido'].widget.attrs['placeholder'] = 'Ingrese sus apellidos'
        self.fields['telefono'].widget.attrs['placeholder'] = 'Ingrese su teléfono'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingrese su correo electrónico'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(FormularioRegistro, self).clean()
        contraseña = cleaned_data.get('contraseña')
        confirmar_contraseña = cleaned_data.get('confirmar_contraseña')

        if contraseña != confirmar_contraseña:
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
