from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from usuarios.models import Usuario, Habilidad
from analisis_mercado.models import OfertaEmpleo
from proyectos.models import Tarea

class RecomendacionTarea(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recomendaciones_tareas'
    )
    tarea = models.ForeignKey(
        Tarea,
        on_delete=models.CASCADE,
        related_name='recomendaciones'
    )
    modelo = models.ForeignKey(
        'ModeloIA',
        on_delete=models.CASCADE,
        related_name='recomendaciones_tareas'
    )
    puntuacion = models.FloatField()  # Score de compatibilidad (0-1)
    razones = models.TextField()  # Explicación de la recomendación
    fecha_recomendacion = models.DateTimeField(auto_now_add=True)
    aceptada = models.BooleanField(null=True)
    feedback = models.TextField(blank=True)

    class Meta:
        verbose_name = _('recomendación de tarea')
        verbose_name_plural = _('recomendaciones de tareas')
        ordering = ['-fecha_recomendacion']
        indexes = [
            models.Index(fields=['usuario', 'fecha_recomendacion']),
            models.Index(fields=['puntuacion']),
        ]

    def __str__(self):
        return f"Recomendación para {self.usuario.username} - {self.tarea.titulo}"

class PrediccionHabilidad(models.Model):
    habilidad = models.ForeignKey(
        Habilidad,
        on_delete=models.CASCADE,
        related_name='predicciones'
    )
    modelo = models.ForeignKey(
        'ModeloIA',
        on_delete=models.CASCADE,
        related_name='predicciones'
    )
    demanda_futura = models.FloatField()
    confianza = models.FloatField()
    periodo_prediccion = models.CharField(max_length=50)
    fecha_prediccion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('predicción de habilidad')
        verbose_name_plural = _('predicciones de habilidades')
        ordering = ['-fecha_prediccion']
        indexes = [
            models.Index(fields=['habilidad', 'fecha_prediccion']),
            models.Index(fields=['confianza']),
        ]
        unique_together = ['habilidad', 'modelo']

    def __str__(self):
        return f"Predicción para {self.habilidad.nombre} - {self.periodo_prediccion}"

class ModeloIA(models.Model):
    class TipoModelo(models.TextChoices):
        RECOMENDACION = 'REC', _('Recomendación')
        PREDICCION = 'PRED', _('Predicción')
        CLASIFICACION = 'CLAS', _('Clasificación')

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TipoModelo.choices)
    descripcion = models.TextField()
    version = models.CharField(max_length=20)
    fecha_entrenamiento = models.DateTimeField(auto_now_add=True)
    metricas = models.JSONField()
    parametros = models.JSONField()
    archivo_modelo = models.FileField(upload_to='modelos_ia/')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_entrenamiento']
        verbose_name = _('modelo de IA')
        verbose_name_plural = _('modelos de IA')

    def __str__(self):
        return f"{self.nombre} v{self.version}"

class Recomendacion(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recomendaciones'
    )
    modelo = models.ForeignKey(
        ModeloIA,
        on_delete=models.CASCADE,
        related_name='recomendaciones'
    )
    tipo = models.CharField(max_length=50)  # Tipo de recomendación (tarea, habilidad, etc.)
    contenido = models.JSONField()  # Contenido de la recomendación
    confianza = models.FloatField()  # Nivel de confianza (0-1)
    aplicada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_aplicacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = _('recomendación')
        verbose_name_plural = _('recomendaciones')

    def __str__(self):
        return f"Recomendación para {self.usuario.username} - {self.tipo}"

class DatosEntrenamiento(models.Model):
    class Tipo(models.TextChoices):
        OFERTAS = 'OFER', _('Ofertas de Empleo')
        TAREAS = 'TARE', _('Tareas')
        USUARIOS = 'USER', _('Usuarios')

    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    datos = models.JSONField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    utilizado = models.BooleanField(default=False)
    fecha_utilizacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = _('datos de entrenamiento')
        verbose_name_plural = _('datos de entrenamiento')

    def __str__(self):
        return f"Datos de {self.get_tipo_display()} - {self.fecha_creacion}"

class MetricasModelo(models.Model):
    modelo = models.ForeignKey(
        ModeloIA,
        on_delete=models.CASCADE,
        related_name='metricas'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    datos_evaluacion = models.JSONField()
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = _('métrica de modelo')
        verbose_name_plural = _('métricas de modelos')

    def __str__(self):
        return f"Métricas de {self.modelo.nombre} - {self.fecha}"

class LogPrediccion(models.Model):
    modelo = models.ForeignKey(
        ModeloIA,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    entrada = models.JSONField()  # Datos de entrada
    salida = models.JSONField()  # Resultados
    tiempo_ejecucion = models.FloatField()  # Tiempo en segundos
    exito = models.BooleanField()
    error = models.TextField(blank=True)

    class Meta:
        verbose_name = _('log de predicción')
        verbose_name_plural = _('logs de predicciones')
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['modelo', 'fecha']),
            models.Index(fields=['exito']),
        ]

    def __str__(self):
        return f"Log de {self.modelo.nombre} - {self.fecha}"
