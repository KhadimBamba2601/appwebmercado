from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario
from .decorators import rol_requerido
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from .forms import RegistroForm, PerfilForm

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

def logout_view(request):
    logout(request)
    return redirect('usuarios:login')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)
    return render(request, 'usuarios/perfil.html', {'form': form})

class ListaUsuarios(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Usuario
    template_name = 'usuarios/lista.html'
    context_object_name = 'usuarios'

    def test_func(self):
        return self.request.user.es_admin()

class EditarUsuario(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Usuario
    form_class = PerfilForm
    template_name = 'usuarios/editar.html'
    success_url = reverse_lazy('lista_usuarios')

    def test_func(self):
        return self.request.user.es_admin()