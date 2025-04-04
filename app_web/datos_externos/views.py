from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuarios.decorators import rol_requerido
from .scraper import scrape_tecnoempleo, guardar_ofertas

@login_required
@rol_requerido('admin')
def importar_ofertas(request):
    if request.method == 'POST':
        ofertas = scrape_tecnoempleo()
        guardar_ofertas(ofertas)
        return render(request, 'datos_externos/importar.html', {'mensaje': f"Importadas {len(ofertas)} ofertas."})
    return render(request, 'datos_externos/importar.html')


from analisis_mercado.models import OfertaEmpleo

@login_required
def lista_ofertas(request):
    ofertas = OfertaEmpleo.objects.all()
    return render(request, 'datos_externos/lista_ofertas.html', {'ofertas': ofertas})