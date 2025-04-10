# proyectos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.decorators import rol_requerido  # Asumo que este decorador verifica roles
from django.contrib import messages
from .models import Proyecto, Tarea
from django import forms
from analisis_mercado.models import Habilidad
from usuarios.models import Usuario

# Formularios con etiquetas en español
class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin']
        labels = {
            'nombre': 'Nombre del Proyecto',
            'descripcion': 'Descripción',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin',
        }
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'estado', 'prioridad', 'fecha_limite', 'colaboradores', 'habilidades_requeridas']
        labels = {
            'titulo': 'Título de la Tarea',
            'descripcion': 'Descripción',
            'estado': 'Estado',
            'prioridad': 'Prioridad',
            'fecha_limite': 'Fecha Límite',
            'colaboradores': 'Colaboradores',
            'habilidades_requeridas': 'Habilidades Requeridas',
        }
        widgets = {
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
            'colaboradores': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'habilidades_requeridas': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

@login_required(login_url='/cuentas/login/')
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
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.gestor = request.user
            proyecto.save()
            messages.success(request, f"El proyecto '{proyecto.nombre}' ha sido creado con éxito.")
            return redirect('proyectos:lista_proyectos')
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = ProyectoForm()
    return render(request, 'proyectos/crear.html', {'form': form, 'titulo': 'Crear Proyecto'})

@login_required(login_url='/cuentas/login/')
@rol_requerido('gestor', 'admin')
def editar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id, gestor=request.user)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, f"El proyecto '{proyecto.nombre}' ha sido actualizado con éxito.")
            return redirect('proyectos:lista_proyectos')
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'proyectos/editar.html', {'form': form, 'proyecto': proyecto, 'titulo': 'Editar Proyecto'})

@login_required(login_url='/cuentas/login/')
@rol_requerido('gestor', 'admin')
def eliminar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id, gestor=request.user)
    if request.method == 'POST':
        proyecto.delete()
        messages.success(request, f"El proyecto '{proyecto.nombre}' ha sido eliminado con éxito.")
        return redirect('proyectos:lista_proyectos')
    return render(request, 'proyectos/eliminar.html', {'proyecto': proyecto, 'titulo': 'Eliminar Proyecto'})

@login_required(login_url='/cuentas/login/')
def detalle_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    tareas = proyecto.tareas.all()
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