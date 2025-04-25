from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from analisis_mercado.models import OfertaEmpleo
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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from usuarios.models import Habilidad

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

    """
    Dashboard principal que muestra estadísticas generales del mercado laboral.
    """
    # Estadísticas generales
    total_ofertas = OfertaEmpleo.objects.count()
    ofertas_por_fuente = OfertaEmpleo.objects.values('fuente').annotate(total=Count('id'))
    empresas_unicas = OfertaEmpleo.objects.values('empresa').distinct().count()
    habilidades_unicas = Habilidad.objects.count()

    # Distribución por tipo de trabajo
    distribucion_tipo = OfertaEmpleo.objects.values('tipo_trabajo').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    tipos_trabajo = [item['tipo_trabajo'] for item in distribucion_tipo]
    distribucion_tipo = [item['count'] for item in distribucion_tipo]

    # Top habilidades
    habilidades_demandadas = Habilidad.objects.annotate(num_ofertas=Count('ofertaempleo')).order_by('-num_ofertas')[:10]
    top_habilidades = Habilidad.objects.annotate(
        count=Count('ofertaempleo')
    ).order_by('-count')[:10]
    
    habilidades_nombres = [h.nombre for h in top_habilidades]
    distribucion_habilidades = [h.count for h in top_habilidades]

    context = {
        'total_ofertas': total_ofertas,
        'ofertas_por_fuente': ofertas_por_fuente,
        'empresas_unicas': empresas_unicas,
        'habilidades_unicas': habilidades_unicas,
        'tipos_trabajo': tipos_trabajo,
        'distribucion_tipo': distribucion_tipo,
        'habilidades_demandadas': habilidades_demandadas,
        'top_habilidades': habilidades_nombres,
        'distribucion_habilidades': distribucion_habilidades,
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
def chat_load_last(request):
    """
    Carga los últimos 3 mensajes del historial del chat del usuario, generando HTML directamente.
    """
    chat_history = request.session.get('chat_history', [])
    last_messages = chat_history[-3:]
    html_messages = ""
    for msg in last_messages:
        html_messages += f'<div class="chat-message user-message">{msg.get("user", "")}</div>'
        html_messages += f'<div class="chat-message bot-message">{msg.get("bot", "")}</div>'
    return JsonResponse({'html': html_messages})

@login_required(login_url='/cuentas/login/')
@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            # Verificar si es una solicitud AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                data = json.loads(request.body.decode('utf-8'))
            else:
                data = request.POST
            
            mensaje = data.get('mensaje', '').strip()
            if not mensaje:
                return JsonResponse({'error': 'Por favor, ingresa un mensaje.'}, status=400)
            
            # Obtener o inicializar el historial de chat desde la sesión
            if 'chat_history' not in request.session:
                request.session['chat_history'] = []

            # Procesar el mensaje
            respuesta = procesar_mensaje(mensaje, request.user)

            # Añadir al historial
            request.session['chat_history'].append({'user': mensaje, 'bot': respuesta})
            # Limitar historial a 50 mensajes
            request.session['chat_history'] = request.session['chat_history'][-50:]
            request.session.modified = True
            
            logger.info(f"Chat - Mensaje: {mensaje}, Respuesta: {respuesta}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'response': respuesta,
                    'html': f'<div class="chat-message user-message">{mensaje}</div><div class="chat-message bot-message">{respuesta}</div>'
                })
            else:
                return render(request, 'chat.html', {'chat_history': request.session['chat_history']})
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al decodificar JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error en chat: {str(e)}")
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)
    else:
        return render(request, 'chat.html', {'chat_history': request.session.get('chat_history', [])})