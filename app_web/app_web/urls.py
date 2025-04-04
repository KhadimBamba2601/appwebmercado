from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('proyectos/', include('proyectos.urls')),
    path('datos/', include('datos_externos.urls')),
    
]