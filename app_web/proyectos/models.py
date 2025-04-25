# proyectos/models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Proyecto(models.Model):
    class Estado(models.TextChoices):
        PLANIFICACION = 'PLAN', _('En Planificación')
        EN_PROGRESO = 'PROG', _('En Progreso')
        COMPLETADO = 'COMP', _('Completado')
        CANCELADO = 'CANC', _('Cancelado')

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin_estimada = models.DateField()
    fecha_fin_real = models.DateField(null=True, blank=True)
    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.PLANIFICACION
    )
    gestor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='proyectos_gestionados'
    )
    colaboradores = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='proyectos_colaboracion'
    )
    habilidades_requeridas = models.ManyToManyField('usuarios.Habilidad')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = _('proyecto')
        verbose_name_plural = _('proyectos')

    def __str__(self):
        return self.titulo

    def porcentaje_completado(self):
        tareas = self.tarea_set.all()
        if not tareas:
            return 0
        completadas = tareas.filter(estado=Tarea.Estado.COMPLETADA).count()
        return (completadas / tareas.count()) * 100

class Tarea(models.Model):
    class Prioridad(models.TextChoices):
        BAJA = 'BAJA', _('Baja')
        MEDIA = 'MEDIA', _('Media')
        ALTA = 'ALTA', _('Alta')
        URGENTE = 'URG', _('Urgente')

    class Estado(models.TextChoices):
        PENDIENTE = 'PEND', _('Pendiente')
        EN_PROGRESO = 'PROG', _('En Progreso')
        COMPLETADA = 'COMP', _('Completada')
        CANCELADA = 'CANC', _('Cancelada')

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name='tareas'
    )
    asignado_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tareas_asignadas'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField()
    fecha_completada = models.DateTimeField(null=True, blank=True)
    prioridad = models.CharField(
        max_length=10,
        choices=Prioridad.choices,
        default=Prioridad.MEDIA
    )
    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )
    habilidades_requeridas = models.ManyToManyField('usuarios.Habilidad')
    fecha_fin_estimada = models.DateField()
    fecha_fin_real = models.DateField(null=True, blank=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-prioridad', 'fecha_fin_estimada']
        verbose_name = _('tarea')
        verbose_name_plural = _('tareas')

    def __str__(self):
        return f"{self.titulo} - {self.proyecto.titulo}"

class Comentario(models.Model):
    tarea = models.ForeignKey(
        Tarea,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = _('comentario')
        verbose_name_plural = _('comentarios')

    def __str__(self):
        return f"Comentario de {self.autor.username} en {self.tarea.titulo}"