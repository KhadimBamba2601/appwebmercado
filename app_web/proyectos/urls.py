from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_proyectos, name='lista_proyectos'),
    path('crear/', views.crear_proyecto, name='crear_proyecto'),
    path('editar/<int:id>/', views.editar_proyecto, name='editar_proyecto'),
    path('eliminar/<int:id>/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('detalle/<int:id>/', views.detalle_proyecto, name='detalle_proyecto'),
]