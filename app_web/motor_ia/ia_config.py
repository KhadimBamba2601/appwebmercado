import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración general del motor de IA
IA_CONFIG = {
    'model_dir': 'modelos',
    'data_dir': 'data',
    'cache_dir': 'cache',
    'random_state': 42,
    'n_jobs': -1  # Usar todos los núcleos disponibles
}

# Configuración del modelo de recomendación
RECOMMENDATION_CONFIG = {
    'algorithm': 'random_forest',
    'params': {
        'n_estimators': 100,
        'max_depth': 10,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'random_state': IA_CONFIG['random_state']
    },
    'features': [
        'habilidades_usuario',
        'experiencia_usuario',
        'tendencias_mercado',
        'demanda_habilidades',
        'salario_promedio'
    ],
    'target': 'recomendacion',
    'train_size': 0.8,
    'test_size': 0.2,
    'validation_size': 0.1,
    'min_samples': 100,
    'confidence_threshold': 0.7
}

# Configuración del modelo de predicción
PREDICTION_CONFIG = {
    'algorithm': 'xgboost',
    'params': {
        'n_estimators': 200,
        'max_depth': 8,
        'learning_rate': 0.1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': IA_CONFIG['random_state']
    },
    'features': [
        'fecha',
        'habilidad',
        'demanda_historica',
        'tendencia',
        'estacionalidad',
        'factores_economicos'
    ],
    'target': 'demanda_futura',
    'horizon': 30,  # Días a predecir
    'train_size': 0.8,
    'test_size': 0.2,
    'validation_size': 0.1,
    'min_samples': 50,
    'confidence_threshold': 0.8
}

# Configuración de preprocesamiento
PREPROCESSING_CONFIG = {
    'text_features': [
        'descripcion',
        'requisitos',
        'titulo'
    ],
    'numerical_features': [
        'salario_min',
        'salario_max',
        'num_postulantes',
        'fecha_publicacion'
    ],
    'categorical_features': [
        'ubicacion',
        'empresa',
        'fuente'
    ],
    'text_processing': {
        'max_features': 1000,
        'min_df': 2,
        'max_df': 0.95
    },
    'numerical_processing': {
        'scaling': 'standard',
        'handle_missing': 'mean'
    },
    'categorical_processing': {
        'encoding': 'onehot',
        'handle_missing': 'mode'
    }
}

# Configuración de evaluación
EVALUATION_CONFIG = {
    'metrics': [
        'accuracy',
        'precision',
        'recall',
        'f1',
        'roc_auc'
    ],
    'cv_folds': 5,
    'scoring': 'f1',
    'n_iter': 10,
    'test_size': 0.2,
    'random_state': IA_CONFIG['random_state']
}

# Configuración de logging
LOG_CONFIG = {
    'filename': 'motor_ia.log',
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# Configuración de almacenamiento
STORAGE_CONFIG = {
    'models_dir': 'modelos',
    'data_dir': 'data',
    'cache_dir': 'cache',
    'backup_dir': 'backup',
    'temp_dir': 'temp'
}

# Configuración de notificaciones
NOTIFICATION_CONFIG = {
    'enabled': True,
    'email': {
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', 587)),
        'username': os.getenv('EMAIL_USERNAME', ''),
        'password': os.getenv('EMAIL_PASSWORD', ''),
        'recipients': os.getenv('NOTIFICATION_EMAILS', '').split(',')
    },
    'notify_on': {
        'training_complete': True,
        'evaluation_complete': True,
        'error': True,
        'warning': False
    }
} 