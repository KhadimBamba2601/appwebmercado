from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuarios.decorators import rol_requerido
from .models import OfertaEmpleo, Habilidad
from django.db.models import Count, Avg, Q, F
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.functions import Cast
from django.db.models import FloatField

# Create your views here.

@login_required
def dashboard(request):
    """
    Dashboard principal que muestra estadísticas generales del mercado laboral.
    """
    # Estadísticas generales
    total_ofertas = OfertaEmpleo.objects.count()
    empresas_unicas = OfertaEmpleo.objects.values('empresa').distinct().count()
    habilidades_unicas = Habilidad.objects.count()

    # Distribución por tipo de trabajo
    distribucion_tipo = OfertaEmpleo.objects.values('tipo_trabajo').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    tipos_trabajo = [item['tipo_trabajo'] for item in distribucion_tipo]
    distribucion_tipo = [item['count'] for item in distribucion_tipo]

    # Top habilidades
    top_habilidades = Habilidad.objects.annotate(
        count=Count('ofertaempleo')
    ).order_by('-count')[:10]
    
    habilidades_nombres = [h.nombre for h in top_habilidades]
    distribucion_habilidades = [h.count for h in top_habilidades]

    context = {
        'total_ofertas': total_ofertas,
        'empresas_unicas': empresas_unicas,
        'habilidades_unicas': habilidades_unicas,
        'tipos_trabajo': tipos_trabajo,
        'distribucion_tipo': distribucion_tipo,
        'top_habilidades': habilidades_nombres,
        'distribucion_habilidades': distribucion_habilidades,
    }
    
    return render(request, 'analisis_mercado/panel_de_control.html', context)

@login_required
def tendencias_habilidades(request):
    """
    Vista que muestra las tendencias de habilidades en el mercado laboral.
    """
    # Obtener ofertas de los últimos 90 días
    fecha_limite = timezone.now() - timedelta(days=90)
    ofertas_recientes = OfertaEmpleo.objects.filter(fecha_publicacion__gte=fecha_limite)
    
    # Habilidades más demandadas por período
    habilidades_por_mes = {}
    for i in range(3):
        mes_actual = timezone.now() - timedelta(days=30*i)
        mes_anterior = mes_actual - timedelta(days=30)
        
        ofertas_mes = ofertas_recientes.filter(
            fecha_publicacion__gte=mes_anterior,
            fecha_publicacion__lt=mes_actual
        )
        
        habilidades_mes = Habilidad.objects.filter(
            ofertaempleo__in=ofertas_mes
        ).annotate(
            num_ofertas=Count('ofertaempleo')
        ).order_by('-num_ofertas')[:10]
        
        habilidades_por_mes[mes_actual.strftime('%B')] = habilidades_mes
    
    context = {
        'habilidades_por_mes': habilidades_por_mes,
    }
    
    return render(request, 'analisis_mercado/tendencias_habilidades.html', context)

@login_required
def comparativa_salarial(request):
    """
    Vista que muestra la comparativa salarial por tipo de trabajo y habilidades.
    """
    # Obtener ofertas con salario
    ofertas_con_salario = OfertaEmpleo.objects.exclude(salario__isnull=True)
    
    # Salarios por tipo de trabajo
    salarios_tipo = ofertas_con_salario.values('tipo_trabajo').annotate(
        salario_promedio=Avg('salario'),
        count=Count('id')
    ).order_by('-salario_promedio')
    
    # Salarios por habilidad
    salarios_habilidad = Habilidad.objects.filter(
        ofertaempleo__in=ofertas_con_salario
    ).annotate(
        salario_promedio=Avg('ofertaempleo__salario'),
        count=Count('ofertaempleo')
    ).order_by('-salario_promedio')[:20]
    
    context = {
        'salarios_tipo': salarios_tipo,
        'salarios_habilidad': salarios_habilidad,
    }
    
    return render(request, 'analisis_mercado/comparativa_salarial.html', context)

@login_required
def busqueda_avanzada(request):
    """
    Vista que permite realizar búsquedas avanzadas de ofertas de empleo.
    """
    if request.method == 'POST':
        # Obtener parámetros de búsqueda
        titulo = request.POST.get('titulo', '')
        ubicacion = request.POST.get('ubicacion', '')
        tipo_trabajo = request.POST.get('tipo_trabajo', '')
        habilidades = request.POST.getlist('habilidades', [])
        salario_min = request.POST.get('salario_min', '')
        salario_max = request.POST.get('salario_max', '')
        
        # Construir query
        query = Q()
        if titulo:
            query &= Q(titulo__icontains=titulo)
        if ubicacion:
            query &= Q(ubicacion__icontains=ubicacion)
        if tipo_trabajo:
            query &= Q(tipo_trabajo=tipo_trabajo)
        if habilidades:
            query &= Q(habilidades__in=habilidades)
        if salario_min:
            query &= Q(salario__gte=salario_min)
        if salario_max:
            query &= Q(salario__lte=salario_max)
        
        # Ejecutar búsqueda
        resultados = OfertaEmpleo.objects.filter(query).distinct()
        
        context = {
            'resultados': resultados,
            'titulo': titulo,
            'ubicacion': ubicacion,
            'tipo_trabajo': tipo_trabajo,
            'habilidades_seleccionadas': habilidades,
            'salario_min': salario_min,
            'salario_max': salario_max,
        }
        
    else:
        context = {}
    
    # Obtener opciones para los filtros
    context['tipos_trabajo'] = OfertaEmpleo.objects.values_list('tipo_trabajo', flat=True).distinct()
    context['habilidades'] = Habilidad.objects.all()
    
    return render(request, 'analisis_mercado/busqueda_avanzada.html', context)
