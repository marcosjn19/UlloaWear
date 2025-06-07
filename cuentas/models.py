from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class AdministradorCuentas(BaseUserManager):
    def crear_usuario(self, nombre, apellido, nombre_usuario, email, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico.')
        if not nombre_usuario:
            raise ValueError('El usuario debe tener un nombre de usuario.')

        usuario = self.model(
            email=self.normalize_email(email),
            nombre_usuario=nombre_usuario,
            nombre=nombre,
            apellido=apellido,
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def crear_superusuario(self, nombre, apellido, email, nombre_usuario, password):
        usuario = self.crear_usuario(
            email=self.normalize_email(email),
            nombre_usuario=nombre_usuario,
            password=password,
            nombre=nombre,
            apellido=apellido,
        )
        usuario.is_admin = True
        usuario.is_active = True
        usuario.is_staff = True
        usuario.is_superadmin = True
        usuario.save(using=self._db)
        return usuario
    
class Cuenta(AbstractBaseUser):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    usuario = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=50)

    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultimo_acceso = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['usuario', 'nombre', 'apellido']

    objects = AdministradorCuentas()

    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(Cuenta, on_delete=models.CASCADE)
    direccion_1 = models.CharField(blank=True, max_length=100)
    direccion_2 = models.CharField(blank=True,max_length=100)
    foto_perfil = models.ImageField(blank=True, upload_to='perfiles')
    ciudad = models.CharField(blank=True, max_length=20)
    estado = models.CharField(blank=True, max_length=20)
    pais = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.usuario.nombre

    def direccion_completa(self):
        return f'{self.direccion_1} {self.direccion_2}'