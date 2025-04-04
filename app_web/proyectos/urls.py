from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_proyectos, name='lista_proyectos'),
    path('crear/', views.crear_proyecto, name='crear_proyecto'),
    path('editar/<int:id>/', views.editar_proyecto, name='editar_proyecto'),
    path('eliminar/<int:id>/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('detalle/<int:id>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('proyecto/<int:proyecto_id>/tareas/crear/', views.crear_tarea, name='crear_tarea'),
    path('tareas/editar/<int:id>/', views.editar_tarea, name='editar_tarea'),
    path('tareas/eliminar/<int:id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('tareas/completar/<int:id>/', views.completar_tarea, name='completar_tarea'),
]