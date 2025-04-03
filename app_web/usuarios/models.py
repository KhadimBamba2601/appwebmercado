from django.contrib.auth.models import AbstractUser
from django.db import models
from analisis_mercado.models import Habilidad

class Usuario(AbstractUser):
    ROL_CHOICES = (
        ('admin', 'Administrador'),
        ('gestor', 'Gestor de Proyectos'),
        ('colaborador', 'Colaborador'),
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='colaborador')
    habilidades = models.ManyToManyField('analisis_mercado.Habilidad', blank=True)

    def es_admin(self):
        return self.rol == 'admin'
    
    def es_gestor(self):
        return self.rol == 'gestor'
    
    def es_colaborador(self):
        return self.rol == 'colaborador'