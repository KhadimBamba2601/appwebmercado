# app_web/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import ofertas_empleo, index, estadisticas, panel_de_control, chat
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('chat/', chat, name='chat'),
    path('panel-de-control/', panel_de_control, name='panel_de_control'),
    path('proyectos/', include(('proyectos.urls', 'proyectos'), namespace='proyectos')),
    path('datos/', include(('datos_externos.urls', 'datos_externos'), namespace='datos_externos')),
    path('ofertas/', ofertas_empleo, name='ofertas_empleo'),
    path('estadisticas/', estadisticas, name='estadisticas'), 
    path('usuarios/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]