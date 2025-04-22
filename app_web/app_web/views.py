# app_web/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from analisis_mercado.models import OfertaEmpleo, Habilidad
from proyectos.models import Proyecto, Tarea
from django.core.paginator import Paginator
from django.contrib import messages
from datos_externos.infojobs_scraper import scrape_infojobs
from datos_externos.tecnoempleo_scraper import scrape_tecnoempleo
from datos_externos.linkedin_scraper import scrape_linkedin
from datos_externos.utils import guardar_ofertas
from django.db.models import Count

# Funciones para verificar roles
def is_admin(user):
    return user.is_authenticated and user.groups.filter(name='Administrador').exists()

def is_gestor(user):
    return user.is_authenticated and user.groups.filter(name='Gestor de Proyectos').exists()

@login_required(login_url='/cuentas/login/')
def index(request):
    context = {
        'titulo': 'Gestión de Tareas y Mercado',
    }
    return render(request, 'index.html', context)

@login_required(login_url='/cuentas/login/')
def ofertas_empleo(request):
    # Obtener todos los objetos por defecto
    ofertas = OfertaEmpleo.objects.all().order_by('-fecha_publicacion', 'titulo')
    habilidades_disponibles = Habilidad.objects.all()
    
    # Manejar importación (POST) - Todos los usuarios autenticados pueden importar
    if request.method == 'POST':
        fuente = request.POST.get('fuente', '').strip()
        titulo_import = request.POST.get('titulo', '').strip()
        ubicacion_import = request.POST.get('ubicacion', '').strip()
        
        try:
            if fuente == 'Todas':
                # Importar desde todas las fuentes
                ofertas_infojobs = scrape_infojobs(titulo=titulo_import, ubicacion=ubicacion_import)
                ofertas_tecnoempleo = scrape_tecnoempleo(titulo=titulo_import, ubicacion=ubicacion_import)
                ofertas_linkedin = scrape_linkedin(titulo=titulo_import, ubicacion=ubicacion_import)
                total_ofertas = ofertas_infojobs + ofertas_tecnoempleo + ofertas_linkedin
                guardar_ofertas(total_ofertas)
                messages.success(request, f"Se importaron {len(total_ofertas)} ofertas de todas las fuentes.")
            elif fuente == 'InfoJobs':
                ofertas_importadas = scrape_infojobs(titulo=titulo_import, ubicacion=ubicacion_import)
                guardar_ofertas(ofertas_importadas)
                messages.success(request, f"Se importaron {len(ofertas_importadas)} ofertas de InfoJobs.")
            elif fuente == 'Tecnoempleo':
                ofertas_importadas = scrape_tecnoempleo(titulo=titulo_import, ubicacion=ubicacion_import)
                guardar_ofertas(ofertas_importadas)
                messages.success(request, f"Se importaron {len(ofertas_importadas)} ofertas de Tecnoempleo.")
            elif fuente == 'LinkedIn':
                ofertas_importadas = scrape_linkedin(titulo=titulo_import, ubicacion=ubicacion_import)
                guardar_ofertas(ofertas_importadas)
                messages.success(request, f"Se importaron {len(ofertas_importadas)} ofertas de LinkedIn.")
            else:
                messages.error(request, "Fuente no válida.")
        except Exception as e:
            messages.error(request, f"Error al importar desde {fuente}: {str(e)}")
    
    # Manejar filtros (GET)
    titulo = request.GET.get('titulo', '').strip()
    ubicacion = request.GET.get('ubicacion', '').strip()
    tipo_trabajo = request.GET.get('tipo_trabajo', '').strip()
    fuente = request.GET.get('fuente', '').strip()
    habilidades = request.GET.getlist('habilidades')
    
    if titulo:
        ofertas = ofertas.filter(titulo__icontains=titulo)
    if ubicacion:
        ofertas = ofertas.filter(ubicacion__icontains=ubicacion)
    if tipo_trabajo:
        ofertas = ofertas.filter(tipo_trabajo__iexact=tipo_trabajo)
    if fuente and fuente != 'Todas':
        ofertas = ofertas.filter(fuente__iexact=fuente)
    if habilidades:
        for habilidad in habilidades:
            ofertas = ofertas.filter(habilidades__nombre=habilidad)
    
    # Paginación
    paginator = Paginator(ofertas, 10)  # 10 ofertas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Contexto
    context = {
        'ofertas': page_obj,
        'habilidades_disponibles': habilidades_disponibles,
        'titulo': titulo,
        'ubicacion': ubicacion,
        'tipo_trabajo': tipo_trabajo,
        'fuente': fuente,
        'habilidades_seleccionadas': habilidades,
        'fuentes_disponibles': ['Todas', 'InfoJobs', 'Tecnoempleo', 'LinkedIn'],
        'tipos_trabajo': ['Remoto', 'Híbrido', 'Presencial', 'No especificado'],
    }
    return render(request, 'ofertas_empleo.html', context)

@login_required(login_url='/cuentas/login/')
@user_passes_test(is_admin, login_url='/ofertas/')
def estadisticas(request):
    # Estadísticas solo para administradores
    total_ofertas = OfertaEmpleo.objects.count()
    ofertas_por_fuente = OfertaEmpleo.objects.values('fuente').annotate(total=Count('id'))
    habilidades_demandadas = Habilidad.objects.annotate(num_ofertas=Count('ofertaempleo')).order_by('-num_ofertas')[:10]
    
    context = {
        'total_ofertas': total_ofertas,
        'ofertas_por_fuente': ofertas_por_fuente,
        'habilidades_demandadas': habilidades_demandadas,
    }
    return render(request, 'estadisticas.html', context)

@login_required(login_url='/cuentas/login/')
def panel_de_control(request):
    # Estadísticas de proyectos
    proyectos_total = Proyecto.objects.count()
    proyectos_por_estado = Proyecto.objects.values('estado').annotate(total=Count('id'))
    
    # Estadísticas de tareas
    tareas_total = Tarea.objects.count()
    tareas_por_prioridad = Tarea.objects.values('prioridad').annotate(total=Count('id'))
    
    # Estadísticas de mercado laboral
    ofertas_total = OfertaEmpleo.objects.count()
    habilidades_demandadas = Habilidad.objects.annotate(num_ofertas=Count('ofertaempleo')).order_by('-num_ofertas')[:5]
    
    context = {
        'proyectos_total': proyectos_total,
        'proyectos_por_estado': proyectos_por_estado,
        'tareas_total': tareas_total,
        'tareas_por_prioridad': tareas_por_prioridad,
        'ofertas_total': ofertas_total,
        'habilidades_demandadas': habilidades_demandadas,
    }
    return render(request, 'panel_de_control.html', context)