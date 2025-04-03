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
@rol_requerido('gestor', 'admin')  # Permitir a gestores y admins
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