from django.shortcuts import render, get_object_or_404
from productos.models import Producto

# Create your views here.
def home ( request ):
    return render(request, 'inicio.html')

def detalles_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle.html', {'producto': producto})