# app_web/urls.py (o appwebmercado/urls.py)
from django.contrib import admin
from django.urls import path, include
from app_web.views import ofertas_empleo, index  # Importamos la vista

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('proyectos/', include(('proyectos.urls', 'proyectos'), namespace='proyectos')),
    path('datos/', include(('datos_externos.urls', 'datos_externos'), namespace='datos_externos')),
    path('ofertas/', ofertas_empleo, name='ofertas_empleo'), 
]