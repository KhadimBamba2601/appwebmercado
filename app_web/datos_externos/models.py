from django.db import models
from django.utils.translation import gettext_lazy as _
from analisis_mercado.models import FuenteDatos, OfertaEmpleo

class ConfiguracionScraping(models.Model):
    fuente = models.OneToOneField(
        FuenteDatos,
        on_delete=models.CASCADE,
        related_name='configuracion_scraping'
    )
    intervalo_actualizacion = models.IntegerField(
        help_text=_('Intervalo en minutos entre actualizaciones')
    )
    ultima_ejecucion = models.DateTimeField(null=True, blank=True)
    siguiente_ejecucion = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    parametros = models.JSONField(
        default=dict,
        help_text=_('Parámetros específicos para el scraping')
    )

    class Meta:
        verbose_name = _('configuración de scraping')
        verbose_name_plural = _('configuraciones de scraping')

    def __str__(self):
        return f"Configuración para {self.fuente.nombre}"

class LogScraping(models.Model):
    class Estados(models.TextChoices):
        INICIADO = 'INICIADO', _('Iniciado')
        EN_PROGRESO = 'EN_PROGRESO', _('En Progreso')
        COMPLETADO = 'COMPLETADO', _('Completado')
        ERROR = 'ERROR', _('Error')
        CANCELADO = 'CANCELADO', _('Cancelado')

    fuente = models.ForeignKey(
        FuenteDatos,
        on_delete=models.CASCADE,
        related_name='logs_scraping'
    )
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=Estados.choices,
        default=Estados.INICIADO
    )
    ofertas_encontradas = models.IntegerField(default=0)
    ofertas_actualizadas = models.IntegerField(default=0)
    ofertas_nuevas = models.IntegerField(default=0)
    errores = models.TextField(blank=True)
    detalles = models.JSONField(
        default=dict,
        help_text=_('Detalles adicionales del proceso')
    )

    class Meta:
        verbose_name = _('log de scraping')
        verbose_name_plural = _('logs de scraping')
        ordering = ['-fecha_inicio']
        indexes = [
            models.Index(fields=['fuente', 'fecha_inicio']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return f"Log de {self.fuente.nombre} - {self.fecha_inicio}"

class CacheOfertas(models.Model):
    oferta = models.OneToOneField(
        OfertaEmpleo,
        on_delete=models.CASCADE,
        related_name='cache'
    )
    datos_raw = models.JSONField(
        help_text=_('Datos originales de la oferta')
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    hash_datos = models.CharField(
        max_length=64,
        help_text=_('Hash de los datos para detectar cambios')
    )

    class Meta:
        verbose_name = _('caché de oferta')
        verbose_name_plural = _('caché de ofertas')
        indexes = [
            models.Index(fields=['fecha_actualizacion']),
            models.Index(fields=['hash_datos']),
        ]

    def __str__(self):
        return f"Cache para {self.oferta.titulo}"

class EstadisticasScraping(models.Model):
    fuente = models.ForeignKey(
        FuenteDatos,
        on_delete=models.CASCADE,
        related_name='estadisticas'
    )
    fecha = models.DateField()
    total_ofertas = models.IntegerField()
    ofertas_activas = models.IntegerField()
    ofertas_nuevas = models.IntegerField()
    tiempo_promedio = models.FloatField(
        help_text=_('Tiempo promedio de scraping en segundos')
    )
    tasa_exito = models.FloatField(
        help_text=_('Porcentaje de éxito en el scraping')
    )

    class Meta:
        verbose_name = _('estadística de scraping')
        verbose_name_plural = _('estadísticas de scraping')
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['fuente', 'fecha']),
        ]
        unique_together = ['fuente', 'fecha']

    def __str__(self):
        return f"Estadísticas de {self.fuente.nombre} - {self.fecha}"
