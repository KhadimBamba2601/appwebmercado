# run_scraper.py
import os
import sys
import django

# Añadir el directorio raíz al path para que Python pueda encontrar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django con scraper_settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_web.datos_externos.scraper_settings')
django.setup()

# Importar y ejecutar la función main del scraper
from app_web.datos_externos.scraper import main

if __name__ == "__main__":
    main()