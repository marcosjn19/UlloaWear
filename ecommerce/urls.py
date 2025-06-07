from django.urls import path # type: ignore

from . import views

urlpatterns = [
    path('', views.home, name='inicio'),
    path('producto/<int:pk>/', views.detalles_producto, name='detalle_producto'),
]

# urlpatterns = [
#     path('', lista_publicacion, name='inicio'),
#     path('pub/<int:pk>/', detalle_publicacion, name='detalle_publicacion'),
# ]
