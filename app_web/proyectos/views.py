# proyectos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Proyecto, Tarea
from django import forms
from analisis_mercado.models import Habilidad
from django.contrib import messages
from .models import Proyecto, Tarea
from usuarios.models import Usuario
from usuarios.decorators import rol_requerido
from django.utils import timezone

# Lista de proyectos predefinidos
PROYECTOS_PREDEFINIDOS = {
    'busqueda_ofertas': {
        'titulo': 'Búsqueda de Ofertas Personalizadas',
        'descripcion': 'Proyecto para buscar y aplicar a ofertas de empleo personalizadas.',
        'tareas': [
            {'titulo': 'Configurar filtros de búsqueda', 'descripcion': 'Establecer habilidades, ubicación y salario deseado.', 'prioridad': 'Baja', 'estado': 'pendiente'},
            {'titulo': 'Apuntarse a ofertas', 'descripcion': 'Seleccionar y aplicar a ofertas en plataformas como InfoJobs, Tecnoempleo y LinkedIn.', 'prioridad': 'Alta', 'estado': 'pendiente'},
            {'titulo': 'Enviar currículum personalizado', 'descripcion': 'Adaptar y enviar currículum para cada oferta.', 'prioridad': 'Media', 'estado': 'pendiente'},
            {'titulo': 'Seguimiento de respuestas', 'descripcion': 'Monitorear y registrar respuestas de las empresas.', 'prioridad': 'Alta', 'estado': 'pendiente'},
        ]
    },
    'optimizacion_perfil': {
        'titulo': 'Optimización de Perfil Laboral',
        'descripcion': 'Mejorar el perfil profesional para aumentar las oportunidades de empleo.',
        'tareas': [
            {'titulo': 'Actualizar currículum', 'descripcion': 'Incorporar habilidades demandadas y experiencia reciente.', 'prioridad': 'Alta', 'estado': 'pendiente'},
            {'titulo': 'Optimizar perfil de LinkedIn', 'descripcion': 'Mejorar la visibilidad y el contenido del perfil.', 'prioridad': 'Media', 'estado': 'pendiente'},
            {'titulo': 'Solicitar recomendaciones', 'descripcion': 'Pedir recomendaciones a colegas y supervisores.', 'prioridad': 'Baja', 'estado': 'pendiente'},
        ]
    },
    'preparacion_entrevistas': {
        'titulo': 'Preparación para Entrevistas',
        'descripcion': 'Prepararse para entrevistas de trabajo de manera efectiva.',
        'tareas': [
            {'titulo': 'Investigar la empresa', 'descripcion': 'Conocer la cultura, valores y noticias recientes de la empresa.', 'prioridad': 'Alta', 'estado': 'pendiente'},
            {'titulo': 'Practicar respuestas a preguntas comunes', 'descripcion': 'Preparar respuestas para preguntas frecuentes en entrevistas.', 'prioridad': 'Media', 'estado': 'pendiente'},
            {'titulo': 'Preparar preguntas para el entrevistador', 'descripcion': 'Formular preguntas relevantes para hacer al final de la entrevista.', 'prioridad': 'Baja', 'estado': 'pendiente'},
        ]
    },
}


# Formularios con etiquetas en español
class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_fin_estimada', 'estado', 'creador', 'colaboradores', 'habilidades_requeridas']
        labels = {
            'titulo': 'Título del Proyecto',
            'descripcion': 'Descripción',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin_estimada': 'Fecha de Fin Estimada',
            'estado': 'Estado',
            'creador': 'Creador del Proyecto',
            'colaboradores': 'Colaboradores',
            'habilidades_requeridas': 'Habilidades Requeridas',
        }
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin_estimada': forms.DateInput(attrs={'type': 'date'}),
            'colaboradores': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'habilidades_requeridas': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'estado', 'prioridad', 'fecha_inicio', 'fecha_fin_estimada', 'asignado_a', 'habilidades_requeridas']
        labels = {
            'titulo': 'Título de la Tarea',
            'descripcion': 'Descripción',
            'estado': 'Estado',
            'prioridad': 'Prioridad',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin_estimada': 'Fecha de Fin Estimada',
            'asignado_a': 'Asignado a',
            'habilidades_requeridas': 'Habilidades Requeridas',
        }
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin_estimada': forms.DateInput(attrs={'type': 'date'}),
            'asignado_a': forms.Select(attrs={'class': 'form-select'}),
            'habilidades_requeridas': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

@login_required(login_url='/cuentas/login/')
@rol_requerido('gestor', 'admin')
def lista_proyectos(request):
    proyectos = Proyecto.objects.all()
    # Filtrar proyectos visibles según rol
    if not request.user.groups.filter(name__in=['Administrador', 'Gestor de Proyectos']).exists():
        proyectos = proyectos.filter(colaboradores=request.user) | proyectos.filter(gestor=request.user)
    proyectos = proyectos.distinct()
    return render(request, 'proyectos/lista.html', {'proyectos': proyectos})

@login_required(login_url='/cuentas/login/')
@rol_requerido('gestor', 'admin')
def crear_proyecto(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin_estimada = request.POST.get('fecha_fin_estimada')
        estado = request.POST.get('estado')
        predefinido = request.POST.get('predefinido')

        try:
            proyecto = Proyecto(
                titulo=titulo,
                descripcion=descripcion,
                creador=request.user,
                fecha_inicio=fecha_inicio,
                fecha_fin_estimada=fecha_fin_estimada,
                estado=estado
            )
            proyecto.save()

            # Si se eligió un proyecto predefinido, crear las tareas asociadas
            if predefinido and predefinido in PROYECTOS_PREDEFINIDOS:
                for tarea_data in PROYECTOS_PREDEFINIDOS[predefinido]['tareas']:
                    Tarea.objects.create(
                        proyecto=proyecto,
                        titulo=tarea_data['titulo'],
                        descripcion=tarea_data['descripcion'],
                        estado=tarea_data['estado'],
                        prioridad=tarea_data['prioridad'],
                        fecha_fin_estimada=timezone.now().date() + timezone.timedelta(days=30)  # Fecha límite de ejemplo
                    )

            messages.success(request, 'Proyecto creado exitosamente.')
            return redirect('proyectos:lista_proyectos')
        except Exception as e:
            messages.error(request, f'Error al crear el proyecto: {str(e)}')

    gestores = Usuario.objects.filter(rol='GESTOR')
    predefinidos = [
        {'clave': clave, 'titulo': data['titulo']}
        for clave, data in PROYECTOS_PREDEFINIDOS.items()
    ]
    return render(request, 'proyectos/crear.html', {'gestores': gestores, 'predefinidos': predefinidos})

@login_required(login_url='/cuentas/login/')
@rol_requerido('gestor', 'admin')
def editar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    # Solo el creador o un administrador pueden editar el proyecto
    if not (request.user == proyecto.creador or request.user.es_administrador()):
        messages.error(request, "No tienes permiso para editar este proyecto.")
        return redirect('proyectos:lista_proyectos')
    
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, f"El proyecto '{proyecto.titulo}' ha sido actualizado con éxito.")
            return redirect('proyectos:lista_proyectos')
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'proyectos/editar.html', {'form': form, 'proyecto': proyecto, 'titulo': 'Editar Proyecto'})

@login_required(login_url='/cuentas/login/')
@rol_requerido('gestor', 'admin')
def eliminar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    # Solo el creador o un administrador pueden eliminar el proyecto
    if not (request.user == proyecto.creador or request.user.es_administrador()):
        messages.error(request, "No tienes permiso para eliminar este proyecto.")
        return redirect('proyectos:lista_proyectos')
    
    if request.method == 'POST':
        proyecto.delete()
        messages.success(request, f"El proyecto '{proyecto.titulo}' ha sido eliminado con éxito.")
        return redirect('proyectos:lista_proyectos')
    return render(request, 'proyectos/eliminar.html', {'proyecto': proyecto, 'titulo': 'Eliminar Proyecto'})

@login_required(login_url='/cuentas/login/')
def detalle_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    tareas = proyecto.tarea_set.all()
    return render(request, 'proyectos/detalle.html', {'proyecto': proyecto, 'tareas': tareas})

@login_required(login_url='/cuentas/login/')
@rol_requerido('gestor', 'admin')
def crear_tarea(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.proyecto = proyecto
            tarea.save()
            form.save_m2m()  # Guarda relaciones muchos-a-muchos
            messages.success(request, f"La tarea '{tarea.titulo}' ha sido creada con éxito.")
            return redirect('proyectos:detalle_proyecto', id=proyecto.id)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = TareaForm()
    return render(request, 'proyectos/crear_tarea.html', {
        'form': form, 'proyecto': proyecto, 'titulo': 'Crear Tarea',
        'usuarios': Usuario.objects.all(), 'habilidades': Habilidad.objects.all()
    })

@login_required(login_url='/cuentas/login/')
def editar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    # Permitir edición solo a gestores, admins o colaboradores asignados
    if not (request.user.groups.filter(name__in=['Administrador', 'Gestor de Proyectos']).exists() or request.user in tarea.colaboradores.all()):
        messages.error(request, "No tienes permiso para editar esta tarea.")
        return redirect('proyectos:detalle_proyecto', id=tarea.proyecto.id)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            messages.success(request, f"La tarea '{tarea.titulo}' ha sido actualizada con éxito.")
            return redirect('proyectos:detalle_proyecto', id=tarea.proyecto.id)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'proyectos/editar_tarea.html', {
        'form': form, 'tarea': tarea, 'titulo': 'Editar Tarea',
        'usuarios': Usuario.objects.all(), 'habilidades': Habilidad.objects.all()
    })

@login_required(login_url='/cuentas/login/')
@rol_requerido('gestor', 'admin')
def eliminar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    proyecto_id = tarea.proyecto.id
    if request.method == 'POST':
        tarea.delete()
        messages.success(request, f"La tarea '{tarea.titulo}' ha sido eliminada con éxito.")
        return redirect('proyectos:detalle_proyecto', id=proyecto_id)
    return render(request, 'proyectos/eliminar_tarea.html', {'tarea': tarea, 'titulo': 'Eliminar Tarea'})

@login_required(login_url='/cuentas/login/')
def completar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    # Solo colaboradores asignados, gestores o admins pueden completar
    if not (request.user.groups.filter(name__in=['Administrador', 'Gestor de Proyectos']).exists() or request.user in tarea.colaboradores.all()):
        messages.error(request, "No tienes permiso para completar esta tarea.")
        return redirect('proyectos:detalle_proyecto', id=tarea.proyecto.id)
    if request.method == 'POST':
        tarea.estado = 'completada'
        tarea.save()
        messages.success(request, f"La tarea '{tarea.titulo}' ha sido marcada como completada.")
        return redirect('proyectos:detalle_proyecto', id=tarea.proyecto.id)
    return render(request, 'proyectos/completar_tarea.html', {'tarea': tarea, 'titulo': 'Completar Tarea'})