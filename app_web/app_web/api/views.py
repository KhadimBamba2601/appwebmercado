from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from analisis_mercado.models import OfertaEmpleo
from usuarios.models import Habilidad
from django.core.serializers import serialize
import json

@require_http_methods(["GET"])
def health_check(request):
    """Endpoint para verificar que la API está funcionando"""
    return JsonResponse({"status": "ok"})

@csrf_exempt
@require_http_methods(["POST"])
def importar_ofertas(request):
    """Endpoint para importar ofertas de empleo"""
    try:
        data = json.loads(request.body)
        ofertas_importadas = []
        
        for oferta_data in data:
            # Crear la oferta
            oferta = OfertaEmpleo.objects.create(**oferta_data)
            ofertas_importadas.append({
                "id": oferta.id,
                "titulo": oferta.titulo,
                "empresa": oferta.empresa
            })
        
        return JsonResponse({
            "message": f"Se importaron {len(ofertas_importadas)} ofertas exitosamente",
            "ofertas": ofertas_importadas
        }, status=201)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=400)

@require_http_methods(["GET", "POST"])
def ofertas_list(request):
    """Lista todas las ofertas o crea una nueva"""
    if request.method == "GET":
        ofertas = OfertaEmpleo.objects.all()
        data = json.loads(serialize('json', ofertas))
        return JsonResponse(data, safe=False)
    else:
        try:
            data = json.loads(request.body)
            oferta = OfertaEmpleo.objects.create(**data)
            return JsonResponse({
                "id": oferta.id,
                "message": "Oferta creada exitosamente"
            }, status=201)
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=400)

@require_http_methods(["GET", "PUT", "DELETE"])
def oferta_detail(request, pk):
    """Obtiene, actualiza o elimina una oferta específica"""
    try:
        oferta = OfertaEmpleo.objects.get(pk=pk)
    except OfertaEmpleo.DoesNotExist:
        return JsonResponse({
            "error": "Oferta no encontrada"
        }, status=404)

    if request.method == "GET":
        data = json.loads(serialize('json', [oferta]))[0]
        return JsonResponse(data)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(oferta, key, value)
            oferta.save()
            return JsonResponse({
                "message": "Oferta actualizada exitosamente"
            })
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=400)
    
    elif request.method == "DELETE":
        oferta.delete()
        return JsonResponse({
            "message": "Oferta eliminada exitosamente"
        })

@require_http_methods(["GET", "POST"])
def habilidades_list(request):
    """Lista todas las habilidades o crea una nueva"""
    if request.method == "GET":
        habilidades = Habilidad.objects.all()
        data = json.loads(serialize('json', habilidades))
        return JsonResponse(data, safe=False)
    else:
        try:
            data = json.loads(request.body)
            habilidad = Habilidad.objects.create(**data)
            return JsonResponse({
                "id": habilidad.id,
                "message": "Habilidad creada exitosamente"
            }, status=201)
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=400)

@require_http_methods(["GET", "PUT", "DELETE"])
def habilidad_detail(request, pk):
    """Obtiene, actualiza o elimina una habilidad específica"""
    try:
        habilidad = Habilidad.objects.get(pk=pk)
    except Habilidad.DoesNotExist:
        return JsonResponse({
            "error": "Habilidad no encontrada"
        }, status=404)

    if request.method == "GET":
        data = json.loads(serialize('json', [habilidad]))[0]
        return JsonResponse(data)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(habilidad, key, value)
            habilidad.save()
            return JsonResponse({
                "message": "Habilidad actualizada exitosamente"
            })
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=400)
    
    elif request.method == "DELETE":
        habilidad.delete()
        return JsonResponse({
            "message": "Habilidad eliminada exitosamente"
        }) 