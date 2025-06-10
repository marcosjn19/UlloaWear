from django.urls import path # type: ignore

from . import views

urlpatterns = [
    path('', views.home, name='inicio'),
    path('producto/<uuid:uuid>/', views.detalles_producto, name='detalle_producto'),
    path('categoria/<uuid:uuid>/', views.categoria, name='categoria'),
    path('buscar/', views.buscar_producto, name='buscar_producto')
]

# urlpatterns = [
#     path('', lista_publicacion, name='inicio'),
#     path('pub/<int:pk>/', detalle_publicacion, name='detalle_publicacion'),
# ]
