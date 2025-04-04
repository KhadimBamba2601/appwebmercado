from django.urls import path
from . import views

urlpatterns = [
    path('importar/', views.importar_ofertas, name='importar_ofertas'),
    path('ofertas/', views.lista_ofertas, name='lista_ofertas'),
]