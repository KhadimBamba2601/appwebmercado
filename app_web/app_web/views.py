# app_web/views.py
from django.shortcuts import render
from analisis_mercado.models import OfertaEmpleo
from django.core.paginator import Paginator

def index(request):
    # Contexto básico para la página principal
    context = {
        'titulo': 'Gestión de Tareas y Mercado',  # Título de tu proyecto
    }
    return render(request, 'index.html', context)

def ofertas_empleo(request):
    titulo = request.GET.get('titulo', '')
    ubicacion = request.GET.get('ubicacion', '')
    tipo_trabajo = request.GET.get('tipo_trabajo', '')

    ofertas = OfertaEmpleo.objects.all().order_by('-fecha_publicacion', 'titulo')
    if titulo:
        ofertas = ofertas.filter(titulo__icontains=titulo)
    if ubicacion:
        ofertas = ofertas.filter(ubicacion__icontains=ubicacion)
    if tipo_trabajo:
        ofertas = ofertas.filter(tipo_trabajo__iexact=tipo_trabajo)

    paginator = Paginator(ofertas, 10)  # 10 ofertas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'ofertas': page_obj,
        'titulo': titulo,
        'ubicacion': ubicacion,
        'tipo_trabajo': tipo_trabajo,
        'tipos_trabajo': ['Remoto', 'Híbrido', 'Presencial', 'No especificado']
    }
    return render(request, 'ofertas_empleo.html', context)