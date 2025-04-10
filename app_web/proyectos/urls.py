# proyectos/urls.py
from django.urls import path
from . import views

app_name = 'proyectos'
urlpatterns = [
    path('', views.lista_proyectos, name='lista_proyectos'),
    path('crear/', views.crear_proyecto, name='crear_proyecto'),
    path('<int:id>/editar/', views.editar_proyecto, name='editar_proyecto'),
    path('<int:id>/eliminar/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('<int:id>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('<int:proyecto_id>/tareas/crear/', views.crear_tarea, name='crear_tarea'),
    path('tareas/<int:id>/editar/', views.editar_tarea, name='editar_tarea'),
    path('tareas/<int:id>/eliminar/', views.eliminar_tarea, name='eliminar_tarea'),
    path('tareas/<int:id>/completar/', views.completar_tarea, name='completar_tarea'),

]