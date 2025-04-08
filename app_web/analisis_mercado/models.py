from django.db import models

class Habilidad(models.Model):
    nombre = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nombre

class OfertaEmpleo(models.Model):
    titulo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100, blank=True)
    habilidades = models.ManyToManyField(Habilidad, blank=True)
    salario = models.CharField(max_length=500, blank=True, null=True)
    fecha_publicacion = models.DateField()
    fuente = models.CharField(max_length=50)  # Ejemplo: "InfoJobs", "Tecnoempleo", "LinkedIn"
    tipo_trabajo = models.CharField(max_length=50, default="No especificado")  # Nuevo campo

    class Meta:
        unique_together = ('titulo', 'empresa')  # Evitar duplicados por título y empresa

    def __str__(self):
        return f"{self.titulo} - {self.empresa} - {self.ubicacion} - {self.fuente}"