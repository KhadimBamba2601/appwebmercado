from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('ofertas/', views.ofertas_list, name='ofertas_list'),
    path('ofertas/importar/', views.importar_ofertas, name='importar_ofertas'),
    path('ofertas/<int:pk>/', views.oferta_detail, name='oferta_detail'),
    path('habilidades/', views.habilidades_list, name='habilidades_list'),
    path('habilidades/<int:pk>/', views.habilidad_detail, name='habilidad_detail'),
] 