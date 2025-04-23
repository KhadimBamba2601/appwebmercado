from django.urls import path
from . import views

app_name = 'analisis_mercado'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tendencias/', views.tendencias_habilidades, name='tendencias_habilidades'),
    path('salarios/', views.comparativa_salarial, name='comparativa_salarial'),
    path('busqueda/', views.busqueda_avanzada, name='busqueda_avanzada'),
] 