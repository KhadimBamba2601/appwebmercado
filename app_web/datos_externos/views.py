from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuarios.decorators import rol_requerido
from .scraper import scrape_tecnoempleo, scrape_infojobs, scrape_linkedin, guardar_ofertas
from analisis_mercado.models import OfertaEmpleo, Habilidad

@login_required
@rol_requerido('admin')
def importar_ofertas(request):
    if request.method == 'POST':
        fuente = request.POST.get('fuente', 'Tecnoempleo')
        titulo = request.POST.get('titulo', '')
        ubicacion = request.POST.get('ubicacion', '')

        if fuente == 'Tecnoempleo':
            ofertas = scrape_tecnoempleo(titulo=titulo, ubicacion=ubicacion)
        elif fuente == 'InfoJobs':
            ofertas = scrape_infojobs(titulo=titulo, ubicacion=ubicacion)
        elif fuente == 'LinkedIn':
            ofertas = scrape_linkedin(titulo=titulo, ubicacion=ubicacion)
        else:
            ofertas = []

        guardar_ofertas(ofertas)
        mensaje = f"Importadas {len(ofertas)} ofertas de {fuente}"
        if titulo or ubicacion:
            mensaje += f" (Título: {titulo}, Ubicación: {ubicacion})"
        return render(request, 'datos_externos/importar.html', {'mensaje': mensaje})
    
    return render(request, 'datos_externos/importar.html')

@login_required
def lista_ofertas(request):
    titulo = request.GET.get('titulo', '')
    empresa = request.GET.get('empresa', '')
    ubicacion = request.GET.get('ubicacion', '')
    fuente = request.GET.get('fuente', '')
    tipo_trabajo = request.GET.get('tipo_trabajo', '')

    ofertas = OfertaEmpleo.objects.all()
    if titulo:
        ofertas = ofertas.filter(titulo__icontains=titulo)
    if empresa:
        ofertas = ofertas.filter(empresa__icontains=empresa)
    if ubicacion:
        ofertas = ofertas.filter(ubicacion__icontains=ubicacion)
    if fuente:
        ofertas = ofertas.filter(fuente__icontains=fuente)
    if tipo_trabajo:
        ofertas = ofertas.filter(tipo_trabajo__iexact=tipo_trabajo)

    # Obtener los valores únicos de tipo_trabajo para el filtro
    tipos_trabajo = OfertaEmpleo.objects.values_list('tipo_trabajo', flat=True).distinct()

    print(f"Ofertas encontradas: {ofertas.count()}")
    return render(request, 'datos_externos/lista_ofertas.html', {
        'ofertas': ofertas,
        'titulo': titulo,
        'empresa': empresa,
        'ubicacion': ubicacion,
        'fuente': fuente,
        'tipo_trabajo': tipo_trabajo,
        'tipos_trabajo': tipos_trabajo
    })
from django.db.models import Avg, Count
@login_required
def analisis_ofertas(request):
    habilidades_count = Habilidad.objects.annotate(num_ofertas=Count('ofertaempleo')).order_by('-num_ofertas')[:10]
    salario_promedio = OfertaEmpleo.objects.filter(salario__isnull=False).aggregate(Avg('salario'))
    return render(request, 'datos_externos/analisis.html', {
        'habilidades': habilidades_count,
        'salario_promedio': salario_promedio
    })