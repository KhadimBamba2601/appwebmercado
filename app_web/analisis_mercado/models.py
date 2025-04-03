from django.db import models

class Habilidad(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

class OfertaEmpleo(models.Model):
    titulo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    habilidades = models.ManyToManyField(Habilidad)
    salario = models.CharField(max_length=50, blank=True, null=True)
    fecha_publicacion = models.DateField()
    fuente = models.CharField(max_length=50)