from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.home, name='inicio'),
]

# urlpatterns = [
#     path('', lista_publicacion, name='inicio'),
#     path('pub/<int:pk>/', detalle_publicacion, name='detalle_publicacion'),
# ]