from django.db import models
from django.urls import reverse

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500, blank=True)
    
    # Nueva relación recursiva
    padre = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategorias'
    )

    def __str__(self):
        if self.padre:
            return f"{self.padre} > {self.nombre}"
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('categoria', kwargs={'pk': self.pk})
    
    def obtener_todas_las_hijas(self):
        hijas = list(self.subcategorias.all())
        for sub in self.subcategorias.all():
            hijas += sub.obtener_todas_las_hijas()
        return hijas
