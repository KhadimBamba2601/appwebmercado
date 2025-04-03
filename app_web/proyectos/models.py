from django.db import models
from usuarios.models import Usuario
from analisis_mercado.models import Habilidad

class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    gestor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='proyectos_gestionados')

class Tarea(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('en_progreso', 'En Progreso'), ('completada', 'Completada')])
    prioridad = models.IntegerField(default=1)
    fecha_limite = models.DateField()
    colaboradores = models.ManyToManyField(Usuario, related_name='tareas_asignadas')
    habilidades_requeridas = models.ManyToManyField('analisis_mercado.Habilidad')