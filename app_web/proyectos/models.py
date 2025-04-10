# proyectos/models.py
from django.db import models
from usuarios.models import Usuario  # Asegúrate de que existe
from analisis_mercado.models import Habilidad

class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    gestor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='proyectos_gestionados')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=(('planificado', 'Planificado'), ('en_progreso', 'En Progreso'), ('completado', 'Completado')),
        default='planificado'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
        ('bloqueada', 'Bloqueada')
    )
    PRIORIDADES = (
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta'),
        (4, 'Urgente')
    )
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    prioridad = models.IntegerField(choices=PRIORIDADES, default=2)
    fecha_limite = models.DateField(null=True, blank=True)
    colaboradores = models.ManyToManyField(Usuario, related_name='tareas_asignadas', blank=True)
    habilidades_requeridas = models.ManyToManyField(Habilidad, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} ({self.proyecto.nombre})"
    
class Comentario(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)