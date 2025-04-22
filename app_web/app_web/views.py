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
from motor_ia.predicciones import predecir_habilidades_tendencia
from motor_ia.chat_processor import procesar_mensaje
import logging

# Configurar logging
logger = logging.getLogger(__name__)

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

@login_required
@rol_requerido('admin')
def importar_ofertas(request):
    if request.method == 'POST':
        fuente = request.POST.get('fuente', 'Tecnoempleo')
        titulo = request.POST.get('titulo', '')
        ubicacion = request.POST.get('ubicacion', '')

        if fuente == 'Tecnoempleo':
            ofertas = scrape_tecnoempleo(titulo=titulo, ubicacion=ubicacion)
        elif fuente == 'InfoJobs':
            ofertas = scrape_infojobs(titulo=titulo, ubicacion=ubicacion)
        elif fuente == 'LinkedIn':
            ofertas = scrape_linkedin(titulo=titulo, ubicacion=ubicacion)
        else:
            ofertas = []

        guardar_ofertas(ofertas)
        mensaje = f"Importadas {len(ofertas)} ofertas de {fuente}"
        if titulo or ubicacion:
            mensaje += f" (Título: {titulo}, Ubicación: {ubicacion})"
        return render(request, 'datos_externos/importar.html', {'mensaje': mensaje})
    
    return render(request, 'datos_externos/importar.html')

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
    logger.info("DEBUG - Entrando en la vista panel_de_control")
    
    # Estadísticas de proyectos
    proyectos_total = Proyecto.objects.count()
    proyectos_por_estado = Proyecto.objects.values('estado').annotate(total=Count('id')).order_by('estado')
    
    # Estadísticas de tareas
    tareas_total = Tarea.objects.count()
    tareas_por_prioridad = Tarea.objects.values('prioridad').annotate(total=Count('id')).order_by('prioridad')
    
    # Estadísticas de mercado laboral (integrando lógica de estadisticas)
    ofertas_total = OfertaEmpleo.objects.count()
    ofertas_por_fuente = OfertaEmpleo.objects.values('fuente').annotate(total=Count('id')).order_by('fuente')
    habilidades_demandadas = Habilidad.objects.annotate(num_ofertas=Count('ofertaempleo')).order_by('-num_ofertas')[:5]
    
    # Habilidades en tendencia
    try:
        habilidades_tendencia = predecir_habilidades_tendencia()
        if isinstance(habilidades_tendencia, dict) and 'error' in habilidades_tendencia:
            messages.warning(request, habilidades_tendencia['error'])
            habilidades_tendencia = []
    except Exception as e:
        messages.error(request, f"Error al obtener habilidades en tendencia: {str(e)}")
        habilidades_tendencia = []
    
    # Depuración: Imprimir datos en consola
    logger.info(f"DEBUG - Proyectos Total: {proyectos_total}")
    logger.info(f"DEBUG - Proyectos por Estado: {list(proyectos_por_estado)}")
    logger.info(f"DEBUG - Tareas Total: {tareas_total}")
    logger.info(f"DEBUG - Tareas por Prioridad: {list(tareas_por_prioridad)}")
    logger.info(f"DEBUG - Ofertas Total: {ofertas_total}")
    logger.info(f"DEBUG - Ofertas por Fuente: {list(ofertas_por_fuente)}")
    logger.info(f"DEBUG - Habilidades Demandadas: {[(h.nombre, h.num_ofertas) for h in habilidades_demandadas]}")
    logger.info(f"DEBUG - Habilidades Tendencia: {habilidades_tendencia}")
    
    # Mensajes si no hay datos
    if proyectos_total == 0:
        messages.warning(request, "No hay proyectos registrados.")
    if tareas_total == 0:
        messages.warning(request, "No hay tareas registradas.")
    if ofertas_total == 0:
        messages.warning(request, "No hay ofertas de empleo registradas.")
    if not habilidades_demandadas:
        messages.warning(request, "No hay habilidades asociadas a ofertas.")
    if not ofertas_por_fuente:
        messages.warning(request, "No hay datos de ofertas por fuente.")
    
    context = {
        'proyectos_total': proyectos_total,
        'proyectos_por_estado': proyectos_por_estado,
        'tareas_total': tareas_total,
        'tareas_por_prioridad': tareas_por_prioridad,
        'ofertas_total': ofertas_total,
        'ofertas_por_fuente': ofertas_por_fuente,
        'habilidades_demandadas': habilidades_demandadas,
        'habilidades_tendencia': habilidades_tendencia,
    }
    logger.info(f"DEBUG - Contexto enviado: {context}")
    return render(request, 'panel_de_control.html', context)

@login_required(login_url='/cuentas/login/')
def chat(request):
    # Obtener o inicializar el historial de chat desde la sesión
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    if request.method == 'POST':
        mensaje = request.POST.get('mensaje', '').strip()
        if not mensaje:
            messages.error(request, "Por favor, ingresa un mensaje.")
        else:
            # Procesar el mensaje
            respuesta = procesar_mensaje(mensaje, request.user)
            # Añadir al historial
            request.session['chat_history'].append({'user': mensaje, 'bot': respuesta})
            # Limitar historial a 50 mensajes para evitar exceso de datos
            request.session['chat_history'] = request.session['chat_history'][-50:]
            request.session.modified = True
            logger.info(f"Chat - Mensaje: {mensaje}, Respuesta: {respuesta}")

    # Pasar el historial al contexto
    context = {
        'chat_history': request.session['chat_history'],
    }
    return render(request, 'chat.html', context)