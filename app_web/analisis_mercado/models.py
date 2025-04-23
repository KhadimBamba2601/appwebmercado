# app_web/analisis_mercado/models.py
from django.db import models

class Habilidad(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100, blank=True, null=True)  # Ej: Frontend, Backend, DevOps
    demanda_actual = models.IntegerField(default=0)  # Contador de ofertas que requieren esta habilidad
    tendencia = models.FloatField(default=0.0)  # Porcentaje de cambio en la demanda

    def __str__(self):
        return self.nombre

class OfertaEmpleo(models.Model):
    FUENTE_CHOICES = (
        ('infojobs', 'InfoJobs'),
        ('tecnoempleo', 'Tecnoempleo'),
        ('linkedin', 'LinkedIn'),
    )
    
    TIPO_CONTRATO_CHOICES = (
        ('indefinido', 'Indefinido'),
        ('temporal', 'Temporal'),
        ('practicas', 'Prácticas'),
        ('otro', 'Otro'),
    )
    
    titulo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    tipo_trabajo = models.CharField(max_length=50)
    tipo_contrato = models.CharField(max_length=20, choices=TIPO_CONTRATO_CHOICES, default='indefinido')
    salario = models.CharField(max_length=100, blank=True, null=True)
    salario_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salario_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    experiencia_min = models.IntegerField(null=True, blank=True)  # Años de experiencia requeridos
    fuente = models.CharField(max_length=100, choices=FUENTE_CHOICES)
    fecha_publicacion = models.DateField()
    fecha_actualizacion = models.DateField(auto_now=True)
    habilidades = models.ManyToManyField(Habilidad, blank=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    descripcion = models.TextField(blank=True)
    requisitos = models.TextField(blank=True)
    numero_postulantes = models.IntegerField(default=0)  # Número de personas que se han postulado
    activa = models.BooleanField(default=True)  # Si la oferta sigue activa

    def __str__(self):
        return f"{self.titulo} - {self.empresa}"

class TendenciaMercado(models.Model):
    habilidad = models.ForeignKey(Habilidad, on_delete=models.CASCADE)
    fecha = models.DateField()
    demanda = models.IntegerField()  # Número de ofertas que requieren esta habilidad
    postulaciones = models.IntegerField()  # Número total de postulaciones para ofertas con esta habilidad
    salario_promedio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        unique_together = ('habilidad', 'fecha')
        
    def __str__(self):
        return f"{self.habilidad.nombre} - {self.fecha}"