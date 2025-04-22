# Archivo: motor_ia/predictions.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from analisis_mercado.models import OfertaEmpleo, Habilidad
import pandas as pd

def predict_trending_skills():
    """
    Predice habilidades demandadas basado prospecto.
    """
    # Obtener datos históricos
    ofertas = OfertaEmpleo.objects.all()
    data = [(oferta.descripcion, [h.nombre for h in oferta.habilidades.all()]) for oferta in ofertas]
    
    # Preparar datos
    descriptions = [d[0] for d in data]
    skills = [d[1] for d in data]
    
    # Vectorizar descripciones
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(descriptions)
    
    # Entrenar un modelo por habilidad (ejemplo simplificado)
    trending_skills = []
    for skill in Habilidad.objects.all():
        y = [1 if skill.nombre in oferta_skills else 0 for oferta_skills in skills]
        if sum(y) < 5:  # Ignorar habilidades con pocos datos
            continue
        model = LogisticRegression()
        model.fit(X, y)
        score = model.score(X, y)  # Usar métrica más robusta en producción
        trending_skills.append({'skill': skill.nombre, 'score': score})
    
    # Ordenar por probabilidad
    trending_skills.sort(key=lambda x: x['score'], reverse=True)
    return trending_skills[:5]  # Top 5 habilidades