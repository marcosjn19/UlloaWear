from django.db import models
from django.urls import reverse # type: ignore

# Create your models here.
class Categoria ( models.Model ):
    nombre = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__ ( self ):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse( 'categoria' )