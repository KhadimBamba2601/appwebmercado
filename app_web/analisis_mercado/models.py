# app_web/analisis_mercado/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class FuenteDatos(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    url_base = models.URLField()
    api_key = models.CharField(max_length=200, blank=True)
    activo = models.BooleanField(default=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre

class OfertaEmpleo(models.Model):
    class TipoContrato(models.TextChoices):
        INDEFINIDO = 'INDEF', _('Indefinido')
        TEMPORAL = 'TEMP', _('Temporal')
        PRACTICAS = 'PRAC', _('Prácticas')
        FORMACION = 'FORM', _('Formación')
        OTRO = 'OTRO', _('Otro')

    titulo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=200)
    salario_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salario_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo_contrato = models.CharField(max_length=10, choices=TipoContrato.choices)
    fecha_publicacion = models.DateTimeField()
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)
    url_original = models.URLField()
    fuente = models.ForeignKey(FuenteDatos, on_delete=models.CASCADE)
    habilidades_requeridas = models.ManyToManyField('usuarios.Habilidad')
    candidatos_inscritos = models.IntegerField(default=0)
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.empresa}"

class AnalisisMercado(models.Model):
    fecha_analisis = models.DateTimeField(auto_now_add=True)
    periodo = models.CharField(max_length=50)  # ej: "2024-Q1"
    habilidades_mas_demandadas = models.JSONField()
    salarios_promedio = models.JSONField()
    tendencias_crecimiento = models.JSONField()
    regiones_mas_activas = models.JSONField()
    
    def __str__(self):
        return f"Análisis de Mercado - {self.periodo}"

class PrediccionMercado(models.Model):
    fecha_prediccion = models.DateTimeField(auto_now_add=True)
    periodo_futuro = models.CharField(max_length=50)  # ej: "2024-Q2"
    habilidades_futuras = models.JSONField()
    salarios_estimados = models.JSONField()
    tendencias_predichas = models.JSONField()
    confianza_prediccion = models.FloatField()
    
    def __str__(self):
        return f"Predicción de Mercado - {self.periodo_futuro}"