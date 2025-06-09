# about/views.py
from django.shortcuts import render # type: ignore
from django.http import Http404 # type: ignore

def sobre(request):
    return render(request, "about/sobre.html")

def ayuda(request):
    return render(request, "about/ayuda.html")

PAGES = {
    # Atención al Cliente
    "politica-devolucion":        "Política de devolución",
    "rastrear-pedido":            "Rastrear pedido",
    "envios-devoluciones":        "Envíos y devoluciones",
    "preguntas-frecuentes":       "Preguntas frecuentes",
    # Quiénes Somos
    "nuestra-historia":           "Nuestra historia",
    "sostenibilidad":             "Sostenibilidad",
    "trabaja-con-nosotros":       "Trabaja con nosotros",
    "prensa":                     "Prensa",
    # Otros Sitios
    "marketplace":                "Marketplace",
    "encuentra-tu-estilo":        "Encuentra tu estilo",
    "app-movil":                  "App móvil",
    "blog":                       "Blog",
}

def info_page(request, page):
    title = PAGES.get(page)
    if not title:
        raise Http404("Página no encontrada")
    return render(request, f"about/info/{page}.html", {
        "title": title,
    })