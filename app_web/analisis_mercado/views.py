from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuarios.decorators import rol_requerido
from .models import OfertaEmpleo, Habilidad
from django.db.models import Count, Avg, Q, F
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.functions import Cast
from django.db.models import FloatField
from django.core.paginator import Paginator

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
def habilidades_demandadas(request):
    """
    Vista que muestra las habilidades más demandadas en el mercado laboral.
    """
    # Obtener ofertas de los últimos 30 días
    fecha_limite = timezone.now() - timedelta(days=30)
    ofertas_recientes = OfertaEmpleo.objects.filter(fecha_publicacion__gte=fecha_limite)
    
    # Habilidades más demandadas
    habilidades_demandadas = Habilidad.objects.filter(
        ofertaempleo__in=ofertas_recientes
    ).annotate(
        num_ofertas=Count('ofertaempleo')
    ).order_by('-num_ofertas')[:20]
    
    context = {
        'habilidades_demandadas': habilidades_demandadas,
    }
    
    return render(request, 'analisis_mercado/habilidades_demandadas.html', context)

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

@login_required
def ofertas_empleo(request):
    """
    Vista que muestra y filtra las ofertas de empleo.
    """
    # Obtener parámetros de filtro
    titulo = request.GET.get('titulo', '')
    empresa = request.GET.get('empresa', '')
    tipo_trabajo = request.GET.get('tipo_trabajo', '')
    habilidades_ids = request.GET.getlist('habilidades', [])
    
    # Construir query
    query = Q()
    if titulo:
        query &= Q(titulo__icontains=titulo)
    if empresa:
        query &= Q(empresa__icontains=empresa)
    if tipo_trabajo:
        query &= Q(tipo_trabajo=tipo_trabajo)
    if habilidades_ids:
        query &= Q(habilidades__id__in=habilidades_ids)
    
    # Obtener ofertas filtradas
    ofertas = OfertaEmpleo.objects.filter(query).distinct().order_by('-fecha_publicacion')
    
    # Paginación
    paginator = Paginator(ofertas, 10)  # 10 ofertas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener opciones para los filtros
    tipos_trabajo = OfertaEmpleo.objects.values_list('tipo_trabajo', flat=True).distinct()
    habilidades = Habilidad.objects.all()
    
    context = {
        'ofertas': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'tipos_trabajo': tipos_trabajo,
        'habilidades': habilidades,
        'titulo': titulo,
        'empresa': empresa,
        'tipo_trabajo': tipo_trabajo,
        'habilidades_seleccionadas': habilidades_ids,
    }
    
    return render(request, 'analisis_mercado/ofertas_empleo.html', context)
