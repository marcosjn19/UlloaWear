# about/urls.py
from django.urls import path # type: ignore
from .views import sobre, ayuda, info_page

urlpatterns = [
    path("", sobre, name="sobre"),         # /about/
    path("ayuda/", ayuda, name="ayuda"),    # /about/ayuda/
    # genérico “/about/info/<slug>/”
    path("info/<slug:page>/", info_page, name="info_page"),
]