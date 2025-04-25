# app_web/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from .views import ofertas_empleo, index, estadisticas, panel_de_control, chat, chat_load_last
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='dashboard/', permanent=False)),
    path('usuarios/', include('usuarios.urls')),
    path('proyectos/', include('proyectos.urls')),
    path('analisis-mercado/', include('analisis_mercado.urls')),
    path('motor-ia/', include('motor_ia.urls')),
    path('datos-externos/', include('datos_externos.urls')),
    path('api/', include('app_web.api.urls')),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('chat/', chat, name='chat'),
    path('chat/load-last/', chat_load_last, name='chat_load_last'),
    path('panel-de-control/', panel_de_control, name='panel_de_control'),
    path('ofertas/', ofertas_empleo, name='ofertas_empleo'),
    path('estadisticas/', estadisticas, name='estadisticas'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)