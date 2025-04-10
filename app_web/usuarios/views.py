from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario
from .decorators import rol_requerido

@login_required
@rol_requerido('admin')
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

@login_required
@rol_requerido('admin')
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        rol = request.POST['rol']
        
        usuario = Usuario.objects.create_user(username=username, email=email, password=password, rol=rol)
        usuario.save()
        messages.success(request, 'Usuario creado exitosamente.')
        return redirect('usuarios:lista_usuarios')
    return render(request, 'usuarios/crear.html', {'roles': Usuario.ROL_CHOICES})

@login_required
@rol_requerido('admin')
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        usuario.username = request.POST['username']
        usuario.email = request.POST['email']
        if request.POST['password']:
            usuario.set_password(request.POST['password'])
        usuario.rol = request.POST['rol']
        usuario.save()
        messages.success(request, 'Usuario actualizado exitosamente.')
        return redirect('usuarios:lista_usuarios')
    return render(request, 'usuarios/editar.html', {'usuario': usuario, 'roles': Usuario.ROL_CHOICES})

@login_required
@rol_requerido('admin')
def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('usuarios:lista_usuarios')
    return render(request, 'usuarios/eliminar.html', {'usuario': usuario})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('usuarios:login')