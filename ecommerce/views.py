from django.shortcuts import render, get_object_or_404, redirect
from productos.models import Producto, Resena, Categoria
from django.contrib import messages
from PIL import Image  # Para validar que sea una imagen
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random

# Create your views here.
def home(request):
    # Cargamos todas las categorías raíz con prefetch de subcategorías
    categorias_raiz = Categoria.objects.prefetch_related('subcategorias').filter(padre=None)
    
    # Cargamos todos los productos
    productos_list = Producto.objects.all().select_related('categoria')

    # Seleccionar un producto aleatorio
    try:
        producto_random = random.choice(productos_list)
    except IndexError:
        producto_random = None

    # Paginado: 12 productos por página
    paginator = Paginator(productos_list, 12)
    page_number = request.GET.get('page')
    
    try:
        productos = paginator.page(page_number)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)

    return render(request, 'inicio.html', {
        'categorias_menu': categorias_raiz,
        'productos': productos,
        'producto_random': producto_random,
    })

def detalles_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    reviews = Resena.objects.filter(producto=producto)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Debes iniciar sesión para dejar una reseña.")
            return redirect('detalle_producto', pk=pk)
        imagen = request.FILES.get('imagen')  # Recibir archivo opcional

        # Validar que la imagen sea realmente una imagen
        if imagen:
            try:
                img = Image.open(imagen)
                img.verify()  # Verifica que sea una imagen válida
            except Exception:
                messages.error(request, "El archivo seleccionado no es una imagen válida.")
                return redirect('detalle_producto', pk=pk)
            
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

    # Obtener todas las categorías hijas recursivamente
    categorias_incluidas = [categoria] + categoria.obtener_todas_las_hijas()

    # Mostrar todos los productos que pertenezcan a la categoría o cualquier hija
    productos = Producto.objects.filter(categoria__in=categorias_incluidas)

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