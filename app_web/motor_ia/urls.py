# motor_ia/urls.py
from django.urls import path
from . import views

app_name = 'motor_ia'
urlpatterns = [
    path('recomendaciones/tarea/<int:tarea_id>/', views.recomendaciones_tarea, name='recomendaciones_tarea'),
    path('habilidades-tendencia/', views.habilidades_tendencia, name='habilidades_tendencia'),
]