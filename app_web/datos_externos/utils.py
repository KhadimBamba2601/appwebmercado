# datos_externos/utils.py
import re
from django.utils import timezone
from app_web.analisis_mercado.models import OfertaEmpleo, Habilidad  # Ajustado

# Patrón para capturar salarios
SALARIO_PATTERN = re.compile(r'(\d+[.,]?\d*\s*(?:€|k|K|$)(?:\s*-\s*\d+[.,]?\d*\s*(?:€|k|K|$))?(?:\s*b?ruto?/[ha]nual)?)', re.IGNORECASE)

# Palabras clave para tipo de trabajo
TIPO_TRABAJO_KEYWORDS = {
    "Remoto": ["remoto", "teletrabajo", "full remote", "100% remoto"],
    "Híbrido": ["híbrido", "hibrido", "hybrid", "parcialmente remoto"],
    "Presencial": ["presencial", "on-site", "en oficina"]
}

def limpiar_ofertas_por_fuente(fuente):
    try:
        num_eliminadas, _ = OfertaEmpleo.objects.filter(fuente=fuente).delete()
        print(f"Eliminadas {num_eliminadas} ofertas antiguas de {fuente}.")
    except Exception as e:
        print(f"Error al eliminar ofertas de {fuente}: {e}")

def guardar_ofertas(ofertas):
    if not ofertas:
        return
    fuente = ofertas[0]['fuente']
    limpiar_ofertas_por_fuente(fuente)
    
    for oferta_data in ofertas:
        oferta, created = OfertaEmpleo.objects.get_or_create(
            titulo=oferta_data['titulo'],
            empresa=oferta_data['empresa'],
            defaults={
                'ubicacion': oferta_data['ubicacion'],
                'salario': oferta_data.get('salario', ''),
                'tipo_trabajo': oferta_data.get('tipo_trabajo', 'No especificado'),
                'fecha_publicacion': oferta_data.get('fecha_publicacion', timezone.now().date()),
                'fuente': oferta_data['fuente']
            }
        )
        for habilidad_nombre in oferta_data['habilidades']:
            habilidad_nombre = str(habilidad_nombre)[:200]
            habilidad, _ = Habilidad.objects.get_or_create(nombre=habilidad_nombre)
            oferta.habilidades.add(habilidad)