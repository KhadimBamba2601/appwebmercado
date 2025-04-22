# motor_ia/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from proyectos.models import Tarea
from .recomendaciones import recomendar_usuarios_tarea
from .predicciones import predecir_habilidades_tendencia
from django.contrib import messages

@login_required(login_url='/cuentas/login/')
def recomendaciones_tarea(request, tarea_id):
    """
    Muestra los usuarios recomendados para una tarea específica.
    """
    resultado = recomendar_usuarios_tarea(tarea_id)
    tarea = None
    try:
        tarea = Tarea.objects.get(id=tarea_id)
    except Tarea.DoesNotExist:
        messages.error(request, "La tarea especificada no existe.")
        return render(request, 'motor_ia/recomendaciones_tarea.html', {'error': "Tarea no encontrada"})

    if isinstance(resultado, dict) and "error" in resultado:
        messages.error(request, resultado["error"])
        return render(request, 'motor_ia/recomendaciones_tarea.html', {'tarea': tarea})

    context = {
        'tarea': tarea,
        'recomendaciones': resultado
    }
    return render(request, 'motor_ia/recomendaciones_tarea.html', context)

@login_required(login_url='/cuentas/login/')
def habilidades_tendencia(request):
    """
    Muestra las habilidades en tendencia en el mercado laboral.
    """
    resultado = predecir_habilidades_tendencia(dias_recientes=30)
    
    if isinstance(resultado, dict) and "error" in resultado:
        messages.error(request, resultado["error"])
        return render(request, 'motor_ia/habilidades_tendencia.html', {'error': resultado["error"]})

    context = {
        'habilidades_tendencia': resultado
    }
    return render(request, 'motor_ia/habilidades_tendencia.html', context)