from django.urls import path
from . import views

app_name = 'analisis_mercado'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tendencias/', views.tendencias_habilidades, name='tendencias_mercado'),
    path('habilidades/', views.habilidades_demandadas, name='habilidades_demandadas'),
    path('ofertas/', views.ofertas_empleo, name='ofertas_empleo'),
    path('busqueda/', views.busqueda_avanzada, name='busqueda_avanzada'),
    path('api/ofertas/importar/', views.importar_ofertas, name='importar_ofertas'),
] 