from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.decorators import rol_requerido
from .models import Proyecto, Tarea
from django import forms

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin']

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'estado', 'prioridad', 'fecha_limite', 'colaboradores', 'habilidades_requeridas']

@login_required
def lista_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'proyectos/lista.html', {'proyectos': proyectos})

@login_required
@rol_requerido('gestor', 'admin')
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.gestor = request.user
            proyecto.save()
            return redirect('lista_proyectos')
    else:
        form = ProyectoForm()
    return render(request, 'proyectos/crear.html', {'form': form})

@login_required
@rol_requerido('gestor', 'admin')
def editar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id, gestor=request.user)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('lista_proyectos')
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'proyectos/editar.html', {'form': form, 'proyecto': proyecto})

@login_required
@rol_requerido('gestor', 'admin')
def eliminar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id, gestor=request.user)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('lista_proyectos')
    return render(request, 'proyectos/eliminar.html', {'proyecto': proyecto})

@login_required
def detalle_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    tareas = proyecto.tareas.all()
    return render(request, 'proyectos/detalle.html', {'proyecto': proyecto, 'tareas': tareas})

@login_required
@rol_requerido('gestor', 'admin')
def crear_tarea(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.proyecto = proyecto
            tarea.save()
            form.save_m2m()  # Guarda las relaciones muchos-a-muchos
            return redirect('detalle_proyecto', id=proyecto.id)
    else:
        form = TareaForm()
    return render(request, 'proyectos/crear_tarea.html', {'form': form, 'proyecto': proyecto})

@login_required
@rol_requerido('gestor', 'admin')
def editar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('detalle_proyecto', id=tarea.proyecto.id)
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'proyectos/editar_tarea.html', {'form': form, 'tarea': tarea})

@login_required
@rol_requerido('gestor', 'admin')
def eliminar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    proyecto_id = tarea.proyecto.id
    if request.method == 'POST':
        tarea.delete()
        return redirect('detalle_proyecto', id=proyecto_id)
    return render(request, 'proyectos/eliminar_tarea.html', {'tarea': tarea})

@login_required
def completar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    if request.method == 'POST':
        tarea.estado = 'completada'
        tarea.save()
        return redirect('detalle_proyecto', id=tarea.proyecto.id)
    return render(request, 'proyectos/completar_tarea.html', {'tarea': tarea})