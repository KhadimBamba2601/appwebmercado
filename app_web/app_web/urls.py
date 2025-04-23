# app_web/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import ofertas_empleo, index, estadisticas, panel_de_control, chat, chat_load_last
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('chat/', chat, name='chat'),
    path('chat/load-last/', chat_load_last, name='chat_load_last'),
    path('panel-de-control/', panel_de_control, name='panel_de_control'),
    path('proyectos/', include('proyectos.urls')),
    path('analisis-mercado/', include('analisis_mercado.urls')),
    path('datos-externos/', include('datos_externos.urls')),
    path('motor-ia/', include('motor_ia.urls')),
    path('ofertas/', ofertas_empleo, name='ofertas_empleo'),
    path('estadisticas/', estadisticas, name='estadisticas'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]