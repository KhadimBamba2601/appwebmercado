from django.db import models
from usuarios.models import Usuario
from analisis_mercado.models import Habilidad, OfertaEmpleo

class Recomendacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    oferta = models.ForeignKey(OfertaEmpleo, on_delete=models.CASCADE)
    puntuacion = models.FloatField()  # Puntuación de la recomendación (0-1)
    razones = models.TextField()  # Explicación de por qué se recomienda
    fecha = models.DateTimeField(auto_now_add=True)
    vista = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-puntuacion', '-fecha']
        
    def __str__(self):
        return f"Recomendación para {usuario.username}: {oferta.titulo}"

class PrediccionHabilidad(models.Model):
    habilidad = models.ForeignKey(Habilidad, on_delete=models.CASCADE)
    fecha_prediccion = models.DateField()
    demanda_predicha = models.IntegerField()  # Demanda predicha para esta habilidad
    confianza = models.FloatField()  # Nivel de confianza en la predicción (0-1)
    tendencia = models.FloatField()  # Tendencia predicha (porcentaje de cambio)
    
    class Meta:
        ordering = ['-fecha_prediccion', '-confianza']
        
    def __str__(self):
        return f"Predicción para {habilidad.nombre} - {fecha_prediccion}"

class ModeloIA(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # 'recomendacion' o 'prediccion'
    version = models.CharField(max_length=20)
    fecha_entrenamiento = models.DateTimeField()
    metricas = models.JSONField()  # Métricas de rendimiento del modelo
    parametros = models.JSONField()  # Parámetros del modelo
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} v{self.version}"
