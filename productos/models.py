from django.db import models
from categorias.models import Categoria
from django.urls import reverse

# Create your models here.

class Producto ( models.Model ):
    nombre      = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(max_length=500, blank=True)
    precio      = models.FloatField()
    imagenes    = models.ImageField(upload_to='productos/')
    stock       = models.IntegerField()
    categoria   = models.ForeignKey(Categoria, null=True, on_delete=models.SET_NULL)

    def get_url ( self ):
        return reverse ( 'detalle_producto', args=[self.pk])
    
    def __str__(self):
        return self.nombre
    
