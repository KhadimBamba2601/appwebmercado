# motor_ia/predicciones.py
from analisis_mercado.models import OfertaEmpleo, Habilidad
from django.db.models import Count
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

def predecir_habilidades_tendencia():
    """
    Predice habilidades en tendencia basadas en todas las ofertas de empleo,
    sin depender de fechas, usando un análisis de frecuencia y clustering.
    """
    try:
        # Obtener todas las ofertas con sus habilidades
        ofertas = OfertaEmpleo.objects.prefetch_related('habilidades').all()
        if not ofertas.exists():
            return {'error': 'No hay ofertas de empleo disponibles para analizar.'}

        # Crear una lista de "documentos" donde cada documento es la lista de habilidades de una oferta
        documentos = []
        for oferta in ofertas:
            habilidades = [h.nombre for h in oferta.habilidades.all()]
            documentos.append(' '.join(habilidades))

        if not documentos:
            return {'error': 'No hay habilidades asociadas a las ofertas.'}

        # Vectorizar habilidades usando TF-IDF
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(documentos)
        feature_names = vectorizer.get_feature_names_out()

        # Aplicar clustering con K-Means para identificar grupos de habilidades
        num_clusters = min(5, len(documentos))  # Limitar clusters
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(X)

        # Calcular relevancia de habilidades por cluster
        habilidades_relevancia = []
        for cluster_id in range(num_clusters):
            cluster_indices = np.where(kmeans.labels_ == cluster_id)[0]
            if len(cluster_indices) == 0:
                continue

            # Sumar los puntajes TF-IDF de las habilidades en el cluster
            cluster_scores = np.sum(X[cluster_indices].toarray(), axis=0)
            for idx, score in enumerate(cluster_scores):
                if score > 0:
                    habilidad = feature_names[idx]
                    habilidades_relevancia.append({
                        'habilidad': habilidad,
                        'num_ofertas': len(cluster_indices),  # Ofertas en el cluster
                        'relevancia': float(score / len(cluster_indices))  # Puntaje promedio
                    })

        # Ordenar por relevancia y limitar a las top 5
        habilidades_relevancia = sorted(habilidades_relevancia, key=lambda x: x['relevancia'], reverse=True)[:5]

        if not habilidades_relevancia:
            return {'error': 'No se encontraron habilidades relevantes.'}

        return habilidades_relevancia

    except Exception as e:
        return {'error': f'Error al predecir habilidades: {str(e)}'}