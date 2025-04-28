import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_CONFIG = {
    'db_name': os.getenv('DB_NAME', 'appwebmercado'),
    'db_user': os.getenv('DB_USER', 'postgres'),
    'db_password': os.getenv('DB_PASSWORD', 'postgres'),
    'db_host': os.getenv('DB_HOST', 'localhost'),
    'db_port': os.getenv('DB_PORT', '5432')
}

# Configuración de la API
API_CONFIG = {
    'base_url': os.getenv('API_BASE_URL', 'http://localhost:8000/api'),
    'timeout': int(os.getenv('API_TIMEOUT', '30'))
}

# Configuración de la interfaz
UI_CONFIG = {
    'window_title': os.getenv('UI_WINDOW_TITLE', 'Gestión de Tareas y Análisis de Mercado'),
    'window_width': int(os.getenv('UI_WINDOW_WIDTH', '1200')),
    'window_height': int(os.getenv('UI_WINDOW_HEIGHT', '800')),
    'theme': os.getenv('UI_THEME', 'light')
}

# Configuración de logging
LOG_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    'file': os.getenv('LOG_FILE', 'app.log')
}

# Configuración de la aplicación
APP_CONFIG = {
    'name': os.getenv('APP_NAME', 'Gestor de Mercado Laboral'),
    'version': os.getenv('APP_VERSION', '1.0.0'),
    'author': os.getenv('APP_AUTHOR', 'Khadim Bamba'),
    'window_title': os.getenv('APP_WINDOW_TITLE', 'Gestor de Mercado Laboral - CRUD'),
    'window_width': int(os.getenv('APP_WINDOW_WIDTH', '1200')),
    'window_height': int(os.getenv('APP_WINDOW_HEIGHT', '800')),
    'theme': os.getenv('APP_THEME', 'light')
}

# Configuración de scraping
SCRAPER_CONFIG = {
    'delay': int(os.getenv('SCRAPER_DELAY', '2')),  # Delay entre requests en segundos
    'timeout': int(os.getenv('SCRAPER_TIMEOUT', '30')),  # Timeout para requests en segundos
    'max_retries': int(os.getenv('SCRAPER_MAX_RETRIES', '3')),  # Máximo número de reintentos
    'user_agent': os.getenv('SCRAPER_USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
}

# Configuración de exportación
EXPORT_CONFIG = {
    'default_format': os.getenv('EXPORT_DEFAULT_FORMAT', 'csv'),
    'supported_formats': os.getenv('EXPORT_SUPPORTED_FORMATS', 'csv,xlsx,json').split(','),
    'export_path': os.getenv('EXPORT_PATH', 'exports')
}

# Configuración de validación
VALIDATION_CONFIG = {
    'max_title_length': int(os.getenv('VALIDATION_MAX_TITLE_LENGTH', '200')),
    'max_description_length': int(os.getenv('VALIDATION_MAX_DESCRIPTION_LENGTH', '1000')),
    'min_salary': int(os.getenv('VALIDATION_MIN_SALARY', '0')),
    'max_salary': int(os.getenv('VALIDATION_MAX_SALARY', '1000000')),
    'date_format': os.getenv('VALIDATION_DATE_FORMAT', '%Y-%m-%d')
} 