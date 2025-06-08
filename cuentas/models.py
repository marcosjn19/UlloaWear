# cuentas/models.py

from django.db import models # type: ignore
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager # type: ignore

# Create your models here.
class AdministradorCuentas(BaseUserManager):
    def create_user(self, nombre="", apellido="",
                    usuario="", email="", password=None):
        return self.crear_usuario(nombre, apellido, usuario, email, password)
    
    def create_superuser(self, nombre, apellido, email, usuario, password):
        return self.crear_superusuario(nombre, apellido, email, usuario, password)
    
    def crear_usuario(self, nombre="", apellido="",
                      usuario="", email="", password=None):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico.")

        # Defaults si vienen vacíos (no dupliques nombres)
        if not usuario:
            usuario = email.split("@")[0]
        if not nombre:
            nombre = "Usuario"
        if not apellido:
            apellido = ""

        user = self.model(
            email=self.normalize_email(email),
            usuario=usuario,
            nombre=nombre,
            apellido=apellido,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def crear_superusuario(self, nombre, apellido, email, usuario, password):
        user = self.crear_usuario(
            email=self.normalize_email(email),
            usuario=usuario,
            password=password,
            nombre=nombre,
            apellido=apellido,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    
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