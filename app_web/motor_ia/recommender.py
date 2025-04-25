import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings
from ..usuarios.models import Usuario, Habilidad
from ..proyectos.models import Tarea
from ..analisis_mercado.models import OfertaEmpleo
from .models import ModeloIA, RecomendacionTarea
import joblib
import logging

logger = logging.getLogger(__name__)

class TaskRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english'
        )
        self.modelo = None
        self.cargar_modelo()

    def cargar_modelo(self):
        """
        Carga el modelo de recomendación más reciente.
        """
        try:
            modelo = ModeloIA.objects.filter(
                tipo='REC',
                activo=True
            ).order_by('-fecha_entrenamiento').first()
            
            if modelo and modelo.archivo_modelo:
                self.modelo = joblib.load(modelo.archivo_modelo.path)
                self.vectorizer = joblib.load(f"{modelo.archivo_modelo.path}_vectorizer")
            else:
                self.entrenar_modelo()
                
        except Exception as e:
            logger.error(f"Error al cargar modelo: {str(e)}")
            self.entrenar_modelo()

    def entrenar_modelo(self):
        """
        Entrena un nuevo modelo de recomendación.
        """
        try:
            # Obtener datos de entrenamiento
            tareas = Tarea.objects.all()
            usuarios = Usuario.objects.all()
            
            # Preparar datos
            tareas_texto = [
                f"{t.titulo} {t.descripcion} {' '.join(h.nombre for h in t.habilidades_requeridas.all())}"
                for t in tareas
            ]
            
            usuarios_texto = [
                f"{' '.join(h.nombre for h in u.habilidades.all())}"
                for u in usuarios
            ]
            
            # Vectorizar textos
            X_tareas = self.vectorizer.fit_transform(tareas_texto)
            X_usuarios = self.vectorizer.transform(usuarios_texto)
            
            # Calcular similitud
            similitud = cosine_similarity(X_usuarios, X_tareas)
            
            # Guardar modelo
            modelo = ModeloIA.objects.create(
                nombre='TaskRecommender',
                tipo='REC',
                version='1.0',
                metricas={'accuracy': 0.0},  # Se actualizará con métricas reales
                parametros={'vectorizer': 'tfidf', 'similarity': 'cosine'}
            )
            
            joblib.dump(similitud, modelo.archivo_modelo.path)
            joblib.dump(self.vectorizer, f"{modelo.archivo_modelo.path}_vectorizer")
            
            self.modelo = similitud
            
        except Exception as e:
            logger.error(f"Error al entrenar modelo: {str(e)}")
            raise

    def recomendar_tareas(self, usuario, n_recomendaciones=5):
        """
        Recomienda tareas para un usuario basándose en sus habilidades.
        """
        try:
            if not self.modelo is not None:
                self.cargar_modelo()
            
            # Obtener índice del usuario
            usuarios = list(Usuario.objects.all())
            try:
                usuario_idx = usuarios.index(usuario)
            except ValueError:
                logger.error(f"Usuario {usuario.username} no encontrado en el modelo")
                return []
            
            # Obtener similitudes para el usuario
            similitudes = self.modelo[usuario_idx]
            
            # Obtener tareas disponibles
            tareas = list(Tarea.objects.filter(estado='PEND'))
            
            # Ordenar por similitud
            indices_recomendados = np.argsort(similitudes)[::-1][:n_recomendaciones]
            
            recomendaciones = []
            for idx in indices_recomendados:
                if idx < len(tareas):
                    tarea = tareas[idx]
                    puntuacion = float(similitudes[idx])
                    
                    # Crear recomendación
                    recomendacion = RecomendacionTarea.objects.create(
                        usuario=usuario,
                        tarea=tarea,
                        modelo=ModeloIA.objects.filter(tipo='REC', activo=True).first(),
                        puntuacion=puntuacion
                    )
                    recomendaciones.append(recomendacion)
            
            return recomendaciones
            
        except Exception as e:
            logger.error(f"Error al recomendar tareas: {str(e)}")
            return []

    def actualizar_recomendaciones(self):
        """
        Actualiza las recomendaciones para todos los usuarios.
        """
        try:
            usuarios = Usuario.objects.filter(rol='COLABORADOR')
            for usuario in usuarios:
                self.recomendar_tareas(usuario)
        except Exception as e:
            logger.error(f"Error al actualizar recomendaciones: {str(e)}") 