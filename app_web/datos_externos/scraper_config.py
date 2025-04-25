import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración general del scraper
SCRAPER_CONFIG = {
    'delay': 2,  # Delay entre requests en segundos
    'timeout': 30,  # Timeout para requests en segundos
    'max_retries': 3,  # Máximo número de reintentos
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Configuración de Tecnoempleo
TECNOEMPLEO_CONFIG = {
    'base_url': 'https://www.tecnoempleo.com',
    'search_url': 'https://www.tecnoempleo.com/buscar-empleo',
    'api_key': os.getenv('TECNOEMPLEO_API_KEY', ''),
    'api_secret': os.getenv('TECNOEMPLEO_API_SECRET', ''),
    'headers': {
        'User-Agent': SCRAPER_CONFIG['user_agent'],
        'Accept': 'application/json'
    }
}

# Configuración de InfoJobs
INFOJOBS_CONFIG = {
    'base_url': 'https://www.infojobs.net',
    'search_url': 'https://www.infojobs.net/jobsearch/search-results/list.xhtml',
    'api_key': os.getenv('INFOJOBS_API_KEY', ''),
    'api_secret': os.getenv('INFOJOBS_API_SECRET', ''),
    'headers': {
        'User-Agent': SCRAPER_CONFIG['user_agent'],
        'Accept': 'application/json'
    }
}

# Configuración de LinkedIn
LINKEDIN_CONFIG = {
    'base_url': 'https://www.linkedin.com',
    'search_url': 'https://www.linkedin.com/jobs/search',
    'username': os.getenv('LINKEDIN_USERNAME', ''),
    'password': os.getenv('LINKEDIN_PASSWORD', ''),
    'headers': {
        'User-Agent': SCRAPER_CONFIG['user_agent']
    }
}

# Configuración de Selenium
SELENIUM_CONFIG = {
    'driver_path': os.getenv('CHROME_DRIVER_PATH', 'chromedriver'),
    'headless': True,
    'window_size': (1920, 1080),
    'implicit_wait': 10,
    'page_load_timeout': 30
}

# Configuración de proxies (opcional)
PROXY_CONFIG = {
    'enabled': False,
    'proxy_list': [],
    'proxy_username': os.getenv('PROXY_USERNAME', ''),
    'proxy_password': os.getenv('PROXY_PASSWORD', '')
}

# Configuración de logging
LOG_CONFIG = {
    'filename': 'scraper.log',
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# Configuración de almacenamiento
STORAGE_CONFIG = {
    'data_dir': 'data',
    'raw_data_dir': 'data/raw',
    'processed_data_dir': 'data/processed',
    'backup_dir': 'data/backup'
}

# Configuración de procesamiento
PROCESSING_CONFIG = {
    'max_skills_per_job': 10,
    'min_salary': 0,
    'max_salary': 1000000,
    'date_format': '%Y-%m-%d',
    'required_fields': [
        'titulo',
        'empresa',
        'ubicacion',
        'descripcion',
        'requisitos',
        'fecha_publicacion',
        'url_original',
        'fuente'
    ]
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
    }
} 