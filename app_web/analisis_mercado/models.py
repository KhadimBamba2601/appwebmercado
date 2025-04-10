# app_web/analisis_mercado/models.py
from django.db import models

class Habilidad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class OfertaEmpleo(models.Model):
    titulo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    tipo_trabajo = models.CharField(max_length=50)
    salario = models.CharField(max_length=100, blank=True, null=True)
    fuente = models.CharField(max_length=100)
    fecha_publicacion = models.DateField()
    habilidades = models.ManyToManyField(Habilidad, blank=True)
    url = models.URLField(max_length=500, blank=True, null=True)  # Campo para la URL

    def __str__(self):
        return self.titulo