# categorias/context_processors.py
from .models import Categoria

def menu_categorias(request):
    categorias = Categoria.objects.filter(padre__isnull=True).prefetch_related('subcategorias')
    return {'categorias_menu': categorias}

def categorias_menu(request):
    return {
        'categorias_menu': Categoria.objects.filter(padre__isnull=True)
    }