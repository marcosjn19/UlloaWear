from django.shortcuts import render, get_object_or_404, redirect
from productos.models import Producto, Resena, Categoria
from django.contrib import messages
from PIL import Image  # Para validar que sea una imagen


# Create your views here.
def home ( request ):
    return render(request, 'inicio.html')

def detalles_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    reviews = Resena.objects.filter(producto=producto)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Debes iniciar sesión para dejar una reseña.")
            return redirect('detalles_producto', pk=pk)
        imagen = request.FILES.get('imagen')  # Recibir archivo opcional

        # Validar que la imagen sea realmente una imagen
        if imagen:
            try:
                img = Image.open(imagen)
                img.verify()  # Verifica que sea una imagen válida
            except Exception:
                messages.error(request, "El archivo seleccionado no es una imagen válida.")
                return redirect('detalles_producto', pk=pk)
            
        calificacion = int(request.POST.get('calificacion'))
        titulo = request.POST.get('titulo')
        resena = request.POST.get('resena', '')

        
        nueva_resena = Resena.objects.create(
            producto=producto,
            user=request.user,
            calificacion=calificacion,
            titulo=titulo,
            resena=resena,
            imagen=imagen  # Se guardará None si no se envió
        )
        nueva_resena.save()

        messages.success(request, "Gracias por tu reseña.")
        return redirect('detalle_producto', pk=pk)

    context = {
        'producto' : producto,
        'reviews'  : reviews,
        'rango_5'  : range(1, 6),
    }
    return render(request, 'productos/detalle.html', context)

def categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    subcategorias = categoria.subcategorias.all()
    productos = Producto.objects.filter(categoria=categoria)

    return render(request, 'categorias/categoria.html', {
        'categoria': categoria,
        'subcategorias': subcategorias,
        'productos': productos,
    })


def buscar_producto(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=query)
    return render(request, 'productos/busqueda.html', {
        'query': query,
        'productos': productos,
    })