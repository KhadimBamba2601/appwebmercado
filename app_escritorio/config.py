import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_CONFIG = {
    'db_name': 'appwebmercado',
    'db_user': 'postgres',
    'db_password': 'postgres',
    'db_host': 'localhost',
    'db_port': '5432'
}

# Configuración de la API
API_CONFIG = {
    'base_url': 'http://localhost:8000/api',
    'timeout': 30
}

# Configuración de la interfaz
UI_CONFIG = {
    'window_title': 'Gestión de Tareas y Análisis de Mercado',
    'window_width': 1200,
    'window_height': 800,
    'theme': 'light'
}

# Configuración de logging
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'app.log'
}

# Configuración de la aplicación
APP_CONFIG = {
    'name': 'Gestor de Mercado Laboral',
    'version': '1.0.0',
    'author': 'Khadim Bamba',
    'window_title': 'Gestor de Mercado Laboral - CRUD',
    'window_width': 1200,
    'window_height': 800,
    'theme': 'light'
}

# Configuración de scraping
SCRAPER_CONFIG = {
    'delay': 2,  # Delay entre requests en segundos
    'timeout': 30,  # Timeout para requests en segundos
    'max_retries': 3,  # Máximo número de reintentos
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Configuración de exportación
EXPORT_CONFIG = {
    'default_format': 'csv',
    'supported_formats': ['csv', 'xlsx', 'json'],
    'export_path': 'exports'
}

# Configuración de validación
VALIDATION_CONFIG = {
    'max_title_length': 200,
    'max_description_length': 1000,
    'min_salary': 0,
    'max_salary': 1000000,
    'date_format': '%Y-%m-%d'
} 