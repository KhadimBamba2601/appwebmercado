import re
from django.utils import timezone
from proyectos.models import Proyecto, Tarea
from analisis_mercado.models import OfertaEmpleo, Habilidad
from motor_ia.predicciones import predecir_habilidades_tendencia
from datos_externos.views import importar_ofertas
from django.db.models import Count
import logging

# Configurar logging
logger = logging.getLogger(__name__)

def procesar_mensaje(mensaje, user):
    """
    Procesa un mensaje del usuario usando palabras clave y expresiones regulares.
    Retorna una respuesta en texto.
    """
    logger.info(f"Procesando mensaje: {mensaje}")
    mensaje_lower = mensaje.lower().strip()
    tokens = mensaje_lower.split()

    # Identificar intenciones específicas
    if any(word in tokens for word in ['crear', 'nuevo', 'añadir']) and 'proyecto' in tokens:
        return crear_proyecto(mensaje, user)
    elif any(word in tokens for word in ['crear', 'nuevo', 'añadir']) and 'tarea' in tokens:
        return crear_tarea(mensaje, user)
    elif any(word in tokens for word in ['mostrar', 'ver', 'cuáles', 'cuantas', 'total']) and any(word in tokens for word in ['proyectos', 'tareas', 'ofertas', 'habilidades']):
        return consultar_estadisticas(mensaje_lower)
    elif any(word in tokens for word in ['importar', 'actualizar']) and 'ofertas' in tokens:
        return importar_ofertas(mensaje_lower)
    elif any(word in tokens for word in ['habilidades', 'tendencia', 'recomendar']):
        return recomendar_habilidades()
    
    # Respuesta por defecto para mensajes no reconocidos
    return "Lo siento, no entendí tu solicitud. Prueba con: 'Crear proyecto X', 'Mostrar total de tareas', o 'Recomendar habilidades'."

def crear_proyecto(mensaje, user):
    try:
        # Extraer nombre del proyecto con regex
        match = re.search(r'(?:crear|nuevo|añadir)\s+proyecto\s+(.+?)(?:\s+con|\s*$)', mensaje, re.IGNORECASE)
        nombre = match.group(1).strip() if match else "Proyecto Nuevo"
        proyecto = Proyecto.objects.create(
            nombre=nombre,
            descripcion="Creado desde el chat",
            gestor=user,
            fecha_inicio=timezone.now(),
            estado="activo"
        )
        return f"Proyecto '{proyecto.nombre}' creado exitosamente."
    except Exception as e:
        return f"Error al crear proyecto: {str(e)}"

def crear_tarea(mensaje, user):
    try:
        # Extraer nombre de la tarea, proyecto y prioridad
        match_tarea = re.search(r'(?:crear|nuevo|añadir)\s+tarea\s+(.+?)(?:\s+al\s+proyecto\s+(.+?))?(?:\s+con\s+prioridad\s+(\d+))?(\s|$)', mensaje, re.IGNORECASE)
        if not match_tarea:
            return "Formato inválido. Usa: 'Crear tarea X al proyecto Y con prioridad Z'."
        
        tarea_nombre = match_tarea.group(1).strip() or "Tarea Nueva"
        proyecto_nombre = match_tarea.group(2).strip() if match_tarea.group(2) else None
        prioridad = int(match_tarea.group(3)) if match_tarea.group(3) else 1
        
        proyecto = Proyecto.objects.filter(gestor=user, nombre__icontains=proyecto_nombre).first() if proyecto_nombre else Proyecto.objects.filter(gestor=user).first()
        if not proyecto:
            return "No se encontró un proyecto para asignar la tarea. Crea un proyecto primero."
        
        tarea = Tarea.objects.create(
            proyecto=proyecto,
            titulo=tarea_nombre,
            descripcion="Creada desde el chat",
            estado="pendiente",
            prioridad=prioridad,
            fecha_limite=timezone.now()
        )
        return f"Tarea '{tarea.titulo}' creada en el proyecto '{proyecto.nombre}'."
    except Exception as e:
        return f"Error al crear tarea: {str(e)}"

def consultar_estadisticas(mensaje):
    tokens = mensaje.split()
    
    if 'proyectos' in tokens:
        total = Proyecto.objects.count()
        return f"Total de proyectos: {total}"
    elif 'tareas' in tokens:
        total = Tarea.objects.count()
        return f"Total de tareas: {total}"
    elif 'ofertas' in tokens:
        total = OfertaEmpleo.objects.count()
        return f"Total de ofertas: {total}"
    elif 'habilidades' in tokens:
        habilidades = Habilidad.objects.annotate(num_ofertas=Count('ofertaempleo')).order_by('-num_ofertas')[:5]
        if not habilidades:
            return "No hay habilidades demandadas."
        response = "Habilidades más demandadas:\n" + '\n'.join([f"- {h.nombre} ({h.num_ofertas} ofertas)" for h in habilidades])
        return response
    else:
        return "No se reconoció la estadística solicitada."

def importar_ofertas(mensaje):
    try:
        fuente = 'Todas'
        if 'infojobs' in mensaje:
            fuente = 'InfoJobs'
        elif 'tecnoempleo' in mensaje:
            fuente = 'Tecnoempleo'
        elif 'linkedin' in mensaje:
            fuente = 'LinkedIn'
        
        importar_ofertas(fuente=fuente)
        return f"Ofertas de {fuente} importadas exitosamente. Revisa el panel de control."
    except Exception as e:
        return f"Error al importar ofertas: {str(e)}"

def recomendar_habilidades():
    habilidades = predecir_habilidades_tendencia()
    if isinstance(habilidades, dict) and 'error' in habilidades:
        return habilidades['error']
    
    response = "Habilidades en tendencia:\n" + '\n'.join([f"- {h['habilidad']} (Relevancia: {h['relevancia']:.2f})" for h in habilidades])
    return response