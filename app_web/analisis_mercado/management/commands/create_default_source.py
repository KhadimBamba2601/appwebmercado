from django.core.management.base import BaseCommand
from analisis_mercado.models import FuenteDatos

class Command(BaseCommand):
    help = 'Crea una fuente de datos por defecto'

    def handle(self, *args, **options):
        fuente, created = FuenteDatos.objects.get_or_create(
            nombre='Manual',
            defaults={
                'url_base': 'http://localhost:8000',
                'activo': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Fuente de datos por defecto creada exitosamente'))
        else:
            self.stdout.write(self.style.SUCCESS('La fuente de datos por defecto ya existe')) 