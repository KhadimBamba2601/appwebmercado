# motor_ia/recomendaciones.py
from proyectos.models import Tarea
from usuarios.models import Usuario
from django.contrib.auth.models import Group

def recomendar_usuarios_tarea(task_id):
    """
    Recomienda usuarios para una tarea basada en habilidades.
    """
    try:
        task = Tarea.objects.get(id=task_id)
        required_skills = set(task.habilidades_requeridas.all())
        
        # Obtener colaboradores (excluyendo Admins y Gestores)
        colaboradores = Usuario.objects.filter(groups__name='Colaborador')
        recomendaciones = []
        
        for user in colaboradores:
            user_skills = set(user.habilidades.all())  # Asumiendo que Usuario tiene un campo habilidades
            matching_skills = required_skills.intersection(user_skills)
            score = len(matching_skills) / len(required_skills) if required_skills else 0
            if score > 0:
                recomendaciones.append({
                    'user': user,
                    'score': score,
                    'matching_skills': matching_skills
                })
        
        # Ordenar por puntaje
        recomendaciones.sort(key=lambda x: x['score'], reverse=True)
        return recomendaciones[:3]  # Top 3 recomendaciones
    except Tarea.DoesNotExist:
        return []