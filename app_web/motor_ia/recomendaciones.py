# motor_ia/recomendaciones.py
from proyectos.models import Tarea
from usuarios.models import Usuario
from django.contrib.auth.models import Group
from django.db.models import Count

def recomendar_usuarios_tarea(tarea_id):
    """
    Recomienda usuarios para una tarea basada en habilidades y carga de trabajo.

    :param tarea_id: ID de la tarea
    :return: Lista de diccionarios con usuarios recomendados, puntaje y habilidades coincidentes
    """
    try:
        tarea = Tarea.objects.get(id=tarea_id)
        habilidades_requeridas = set(tarea.habilidades_requeridas.all())
        if not habilidades_requeridas:
            return {"error": "La tarea no tiene habilidades requeridas definidas."}

        # Obtener colaboradores (excluyendo Admins y Gestores)
        colaboradores = Usuario.objects.filter(rol=Usuario.Rol.COLABORADOR).annotate(
            num_tareas=Count('tarea__id', distinct=True)
        )
        recomendaciones = []

        for usuario in colaboradores:
            habilidades_usuario = set(usuario.habilidades.all())
            habilidades_coincidentes = habilidades_requeridas.intersection(habilidades_usuario)
            if not habilidades_coincidentes:
                continue

            # Calcular puntaje: 70% habilidades, 30% carga de trabajo
            puntaje_habilidades = len(habilidades_coincidentes) / len(habilidades_requeridas)
            puntaje_carga = 1 - (min(usuario.num_tareas, 10) / 10)  # Normalizar carga (máx. 10 tareas)
            puntaje_total = 0.7 * puntaje_habilidades + 0.3 * puntaje_carga

            recomendaciones.append({
                'usuario': usuario,
                'puntaje': puntaje_total,
                'habilidades_coincidentes': habilidades_coincidentes,
                'num_tareas': usuario.num_tareas
            })

        # Ordenar por puntaje y limitar a los 3 mejores
        recomendaciones.sort(key=lambda x: x['puntaje'], reverse=True)
        if not recomendaciones:
            return {"error": "No se encontraron usuarios con habilidades adecuadas."}
        
        return recomendaciones[:3]

    except Tarea.DoesNotExist:
        return {"error": "La tarea especificada no existe."}
    except Exception as e:
        return {"error": f"Error al generar recomendaciones: {str(e)}"}