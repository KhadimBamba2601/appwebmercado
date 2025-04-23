import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from django.db.models import Count, Avg
from .models import Recomendacion, PrediccionHabilidad, ModeloIA
from usuarios.models import Usuario
from analisis_mercado.models import Habilidad, OfertaEmpleo, TendenciaMercado

class ServicioIA:
    def __init__(self):
        self.modelo_recomendacion = None
        self.modelo_prediccion = None
        self.vectorizador = TfidfVectorizer()
        
    def entrenar_modelo_recomendacion(self):
        """Entrena el modelo de recomendación basado en habilidades y ofertas"""
        # Obtener todas las ofertas activas
        ofertas = OfertaEmpleo.objects.filter(activa=True)
        
        # Crear matriz de características
        habilidades_texto = [' '.join([h.nombre for h in o.habilidades.all()]) for o in ofertas]
        matriz_caracteristicas = self.vectorizador.fit_transform(habilidades_texto)
        
        # Guardar modelo
        modelo = ModeloIA.objects.create(
            nombre='Sistema de Recomendación',
            tipo='recomendacion',
            version='1.0',
            fecha_entrenamiento=datetime.now(),
            metricas={'status': 'entrenado'},
            parametros={'vectorizador': 'TfidfVectorizer'}
        )
        self.modelo_recomendacion = modelo
        
    def generar_recomendaciones(self, usuario):
        """Genera recomendaciones de ofertas para un usuario"""
        if not self.modelo_recomendacion:
            self.entrenar_modelo_recomendacion()
            
        # Obtener habilidades del usuario
        habilidades_usuario = ' '.join([h.nombre for h in usuario.habilidades.all()])
        vector_usuario = self.vectorizador.transform([habilidades_usuario])
        
        # Obtener ofertas activas
        ofertas = OfertaEmpleo.objects.filter(activa=True)
        habilidades_ofertas = [' '.join([h.nombre for h in o.habilidades.all()]) for o in ofertas]
        matriz_ofertas = self.vectorizador.transform(habilidades_ofertas)
        
        # Calcular similitud
        similitudes = cosine_similarity(vector_usuario, matriz_ofertas)[0]
        
        # Crear recomendaciones
        recomendaciones = []
        for i, oferta in enumerate(ofertas):
            if similitudes[i] > 0.1:  # Umbral mínimo de similitud
                recomendacion = Recomendacion.objects.create(
                    usuario=usuario,
                    oferta=oferta,
                    puntuacion=float(similitudes[i]),
                    razones=f"Similitud de habilidades: {similitudes[i]:.2f}"
                )
                recomendaciones.append(recomendacion)
                
        return recomendaciones
        
    def entrenar_modelo_prediccion(self):
        """Entrena el modelo de predicción de tendencias"""
        # Obtener datos históricos
        tendencias = TendenciaMercado.objects.all()
        
        # Preparar datos para el modelo
        X = []
        y = []
        for t in tendencias:
            X.append([t.fecha.toordinal()])
            y.append(t.demanda)
            
        X = np.array(X)
        y = np.array(y)
        
        # Entrenar modelo
        modelo = LinearRegression()
        modelo.fit(X, y)
        
        # Guardar modelo
        modelo_ia = ModeloIA.objects.create(
            nombre='Predicción de Demanda',
            tipo='prediccion',
            version='1.0',
            fecha_entrenamiento=datetime.now(),
            metricas={'r2_score': float(modelo.score(X, y))},
            parametros={'modelo': 'LinearRegression'}
        )
        self.modelo_prediccion = modelo
        
    def predecir_tendencias(self, dias_futuro=30):
        """Predice tendencias de habilidades para los próximos días"""
        if not self.modelo_prediccion:
            self.entrenar_modelo_prediccion()
            
        # Obtener fecha actual y futura
        fecha_actual = datetime.now().date()
        fecha_futura = fecha_actual + timedelta(days=dias_futuro)
        
        # Predecir para cada habilidad
        habilidades = Habilidad.objects.all()
        predicciones = []
        
        for habilidad in habilidades:
            # Obtener datos históricos de la habilidad
            tendencias = TendenciaMercado.objects.filter(habilidad=habilidad)
            if not tendencias:
                continue
                
            # Preparar datos
            X = np.array([[t.fecha.toordinal()] for t in tendencias])
            y = np.array([t.demanda for t in tendencias])
            
            # Entrenar modelo específico para esta habilidad
            modelo = LinearRegression()
            modelo.fit(X, y)
            
            # Predecir demanda futura
            fecha_futura_ordinal = fecha_futura.toordinal()
            demanda_predicha = modelo.predict([[fecha_futura_ordinal]])[0]
            
            # Calcular tendencia
            demanda_actual = tendencias.order_by('-fecha').first().demanda
            tendencia = (demanda_predicha - demanda_actual) / demanda_actual if demanda_actual > 0 else 0
            
            # Crear predicción
            prediccion = PrediccionHabilidad.objects.create(
                habilidad=habilidad,
                fecha_prediccion=fecha_futura,
                demanda_predicha=int(demanda_predicha),
                confianza=float(modelo.score(X, y)),
                tendencia=float(tendencia)
            )
            predicciones.append(prediccion)
            
        return predicciones 