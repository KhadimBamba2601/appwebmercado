from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrador')
        GESTOR = 'GESTOR', _('Gestor de Proyectos')
        COLABORADOR = 'COLABORADOR', _('Colaborador')

    rol = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.COLABORADOR
    )
    habilidades = models.ManyToManyField('Habilidad', blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()})"

    def es_administrador(self):
        return self.rol == self.Roles.ADMIN

    def es_gestor(self):
        return self.rol == self.Roles.GESTOR

    def es_colaborador(self):
        return self.rol == self.Roles.COLABORADOR

class Habilidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.nombre