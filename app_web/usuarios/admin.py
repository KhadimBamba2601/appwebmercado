from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    # Campos que se muestran en el formulario de edición
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
        ('Campos personalizados', {'fields': ('rol', 'habilidades')}),  # Añadimos rol y habilidades
    )
    # Campos que se muestran en la lista de usuarios
    list_display = ('username', 'email', 'rol', 'is_staff')
    # Filtros en la barra lateral
    list_filter = ('rol', 'is_staff', 'is_superuser')
    # Campos buscables
    search_fields = ('username', 'email')

admin.site.register(Usuario, UsuarioAdmin)