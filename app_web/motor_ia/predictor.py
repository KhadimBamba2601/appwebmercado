import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from django.conf import settings
from ..usuarios.models import Habilidad
from ..analisis_mercado.models import OfertaEmpleo, PrediccionMercado
from .models import ModeloIA
import joblib
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class MarketPredictor:
    def __init__(self):
        self.modelo = None
        self.scaler = None
        self.cargar_modelo()

    def cargar_modelo(self):
        """
        Carga el modelo de predicción más reciente.
        """
        try:
            modelo = ModeloIA.objects.filter(
                tipo='PRED',
                activo=True
            ).order_by('-fecha_entrenamiento').first()
            
            if modelo and modelo.archivo_modelo:
                self.modelo = joblib.load(modelo.archivo_modelo.path)
                self.scaler = joblib.load(f"{modelo.archivo_modelo.path}_scaler")
            else:
                self.entrenar_modelo()
                
        except Exception as e:
            logger.error(f"Error al cargar modelo: {str(e)}")
            self.entrenar_modelo()

    def preparar_datos(self):
        """
        Prepara los datos históricos para el entrenamiento.
        """
        try:
            # Obtener ofertas históricas
            ofertas = OfertaEmpleo.objects.all().order_by('fecha_publicacion')
            
            # Crear DataFrame
            data = []
            for oferta in ofertas:
                for habilidad in oferta.habilidades_requeridas.all():
                    data.append({
                        'fecha': oferta.fecha_publicacion,
                        'habilidad': habilidad.nombre,
                        'salario': oferta.salario_max or oferta.salario_min or 0,
                        'ubicacion': oferta.ubicacion,
                        'tipo_contrato': oferta.tipo_contrato
                    })
            
            df = pd.DataFrame(data)
            
            # Agregar características temporales
            df['year'] = df['fecha'].dt.year
            df['month'] = df['fecha'].dt.month
            df['quarter'] = df['fecha'].dt.quarter
            
            # Codificar variables categóricas
            df = pd.get_dummies(df, columns=['habilidad', 'ubicacion', 'tipo_contrato'])
            
            return df
            
        except Exception as e:
            logger.error(f"Error al preparar datos: {str(e)}")
            return None

    def entrenar_modelo(self):
        """
        Entrena un nuevo modelo de predicción.
        """
        try:
            # Preparar datos
            df = self.preparar_datos()
            if df is None or df.empty:
                raise ValueError("No hay datos suficientes para entrenar el modelo")
            
            # Separar características y objetivo
            X = df.drop(['fecha', 'salario'], axis=1)
            y = df['salario']
            
            # Escalar características
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            
            # Entrenar modelo
            self.modelo = RandomForestRegressor(
                n_estimators=100,
                random_state=42
            )
            self.modelo.fit(X_scaled, y)
            
            # Guardar modelo
            modelo = ModeloIA.objects.create(
                nombre='MarketPredictor',
                tipo='PRED',
                version='1.0',
                metricas={
                    'r2_score': self.modelo.score(X_scaled, y)
                },
                parametros={
                    'n_estimators': 100,
                    'random_state': 42
                }
            )
            
            joblib.dump(self.modelo, modelo.archivo_modelo.path)
            joblib.dump(self.scaler, f"{modelo.archivo_modelo.path}_scaler")
            
        except Exception as e:
            logger.error(f"Error al entrenar modelo: {str(e)}")
            raise

    def predecir_mercado(self, periodo_futuro):
        """
        Realiza predicciones para el mercado laboral.
        """
        try:
            if self.modelo is None:
                self.cargar_modelo()
            
            # Obtener habilidades actuales
            habilidades = Habilidad.objects.all()
            
            # Preparar datos para predicción
            fecha_futura = datetime.strptime(periodo_futuro, '%Y-Q%q')
            datos_prediccion = []
            
            for habilidad in habilidades:
                datos_prediccion.append({
                    'year': fecha_futura.year,
                    'month': fecha_futura.month,
                    'quarter': fecha_futura.quarter,
                    'habilidad': habilidad.nombre
                })
            
            df_pred = pd.DataFrame(datos_prediccion)
            df_pred = pd.get_dummies(df_pred, columns=['habilidad'])
            
            # Escalar características
            X_pred = self.scaler.transform(df_pred)
            
            # Realizar predicciones
            predicciones = self.modelo.predict(X_pred)
            
            # Calcular confianza
            confianza = np.mean([
                tree.predict(X_pred).std() 
                for tree in self.modelo.estimators_
            ])
            
            # Crear predicción en la base de datos
            prediccion = PrediccionMercado.objects.create(
                periodo_futuro=periodo_futuro,
                habilidades_futuras={
                    h.nombre: float(p) 
                    for h, p in zip(habilidades, predicciones)
                },
                confianza_prediccion=float(confianza)
            )
            
            return prediccion
            
        except Exception as e:
            logger.error(f"Error al predecir mercado: {str(e)}")
            return None

    def actualizar_predicciones(self):
        """
        Actualiza las predicciones para el próximo trimestre.
        """
        try:
            # Calcular próximo trimestre
            hoy = datetime.now()
            proximo_trimestre = (hoy.month - 1) // 3 + 1
            proximo_año = hoy.year
            
            if proximo_trimestre == 4:
                proximo_trimestre = 1
                proximo_año += 1
            
            periodo = f"{proximo_año}-Q{proximo_trimestre}"
            self.predecir_mercado(periodo)
            
        except Exception as e:
            logger.error(f"Error al actualizar predicciones: {str(e)}") 