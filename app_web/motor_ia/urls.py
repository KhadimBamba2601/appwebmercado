from django.urls import path, include

app_name = 'motor_ia'
urlpatterns = [
    path('ia/', include('motor_ia.urls'))
]