from django.db import models
from categorias.models import Categoria
from cuentas.models import Cuenta
from django.urls import reverse
from django.db.models import Avg, Count
import uuid
# Create your models here.

class Producto ( models.Model ):
    uuid        = models.UUIDField(
                    default      = uuid.uuid4,
                    editable     = False,
                    unique       = True
                )
    nombre      = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(max_length=500, blank=True)
    precio      = models.FloatField()
    imagenes    = models.ImageField(upload_to='productos/')
    stock       = models.IntegerField()
    categoria   = models.ForeignKey(Categoria, null=True, on_delete=models.SET_NULL)

    def get_url ( self ):
        return reverse ( 'detalle_producto', args=[str(self.uuid)])
    
    def __str__(self):
        return self.nombre
    
    def averageReview(self):
        reviews = Resena.objects.filter(producto=self).aggregate(average=Avg('calificacion'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = Resena.objects.filter(producto=self).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
class Resena(models.Model):
    producto = models.ForeignKey(Producto, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(Cuenta, null=True, on_delete=models.CASCADE)
    calificacion = models.IntegerField()
    titulo = models.TextField(max_length=255)
    resena = models.TextField(max_length=500, blank=True)
    imagen = models.ImageField(upload_to='reseñas/', null=True, blank=True)  # Nueva línea
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo