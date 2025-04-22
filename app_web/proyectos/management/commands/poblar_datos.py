from django.core.management.base import BaseCommand
from django.utils import timezone
from usuarios.models import Usuario
from proyectos.models import Proyecto, Tarea
from analisis_mercado.models import Habilidad

class Command(BaseCommand):
    help = 'Pobla la base de datos con proyectos y tareas predefinidos'

    def handle(self, *args, **kwargs):
        # Verificar si hay un admin para asignar como gestor
        try:
            admin = Usuario.objects.get(rol='admin')
        except Usuario.DoesNotExist:
            self.stdout.write(self.style.ERROR('No hay usuarios con rol "admin". Crea uno primero.'))
            return

        # Crear habilidades si no existen
        habilidades = ['Python', 'Django', 'Análisis de Datos', 'Diseño UX', 'Scraping']
        habilidades_objs = []
        for nombre in habilidades:
            habilidad, _ = Habilidad.objects.get_or_create(nombre=nombre)
            habilidades_objs.append(habilidad)

        # Proyectos predefinidos
        proyectos_data = [
            {
                'nombre': 'Desarrollo de Plataforma Web',
                'descripcion': 'Crear una plataforma web para gestionar tareas y proyectos.',
                'fecha_inicio': timezone.now().date(),
                'fecha_fin': timezone.now().date() + timezone.timedelta(days=90),
                'estado': 'pendiente',
                'tareas': [
                    {
                        'titulo': 'Diseñar mockups',
                        'descripcion': 'Crear diseños iniciales en Figma.',
                        'estado': 'pendiente',
                        'prioridad': 3,  # Alta
                        'fecha_limite': timezone.now().date() + timezone.timedelta(days=15),
                        'habilidades': ['Diseño UX'],
                    },
                    {
                        'titulo': 'Implementar backend',
                        'descripcion': 'Desarrollar la lógica del servidor con Django.',
                        'estado': 'pendiente',
                        'prioridad': 2,  # Media
                        'fecha_limite': timezone.now().date() + timezone.timedelta(days=45),
                        'habilidades': ['Python', 'Django'],
                    },
                ],
            },
            {
                'nombre': 'Análisis de Mercado Laboral',
                'descripcion': 'Recolectar y analizar datos de ofertas de empleo.',
                'fecha_inicio': timezone.now().date(),
                'fecha_fin': timezone.now().date() + timezone.timedelta(days=60),
                'estado': 'pendiente',
                'tareas': [
                    {
                        'titulo': 'Configurar scrapers',
                        'descripcion': 'Implementar scrapers para InfoJobs y LinkedIn.',
                        'estado': 'pendiente',
                        'prioridad': 3,  # Alta
                        'fecha_limite': timezone.now().date() + timezone.timedelta(days=20),
                        'habilidades': ['Python', 'Scraping'],
                    },
                    {
                        'titulo': 'Analizar datos',
                        'descripcion': 'Generar reportes de habilidades demandadas.',
                        'estado': 'pendiente',
                        'prioridad': 2,  # Media
                        'fecha_limite': timezone.now().date() + timezone.timedelta(days=40),
                        'habilidades': ['Análisis de Datos'],
                    },
                ],
            },
        ]

        # Crear proyectos y tareas
        for proyecto_data in proyectos_data:
            proyecto, created = Proyecto.objects.get_or_create(
                nombre=proyecto_data['nombre'],
                defaults={
                    'descripcion': proyecto_data['descripcion'],
                    'gestor': admin,
                    'fecha_inicio': proyecto_data['fecha_inicio'],
                    'fecha_fin': proyecto_data['fecha_fin'],
                    'estado': proyecto_data['estado'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Proyecto "{proyecto.nombre}" creado.'))
            else:
                self.stdout.write(self.style.WARNING(f'Proyecto "{proyecto.nombre}" ya existía.'))

            # Crear tareas
            for tarea_data in proyecto_data['tareas']:
                tarea, created = Tarea.objects.get_or_create(
                    proyecto=proyecto,
                    titulo=tarea_data['titulo'],
                    defaults={
                        'descripcion': tarea_data['descripcion'],
                        'estado': tarea_data['estado'],
                        'prioridad': tarea_data['prioridad'],
                        'fecha_limite': tarea_data['fecha_limite'],
                    }
                )
                if created:
                    # Asignar habilidades
                    for habilidad_nombre in tarea_data['habilidades']:
                        habilidad = Habilidad.objects.get(nombre=habilidad_nombre)
                        tarea.habilidades_requeridas.add(habilidad)
                    self.stdout.write(self.style.SUCCESS(f'Tarea "{tarea.titulo}" creada en "{proyecto.nombre}".'))
                else:
                    self.stdout.write(self.style.WARNING(f'Tarea "{tarea.titulo}" ya existía en "{proyecto.nombre}".'))

        self.stdout.write(self.style.SUCCESS('Poblado completado.'))