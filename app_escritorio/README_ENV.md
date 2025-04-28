# Configuración de Variables de Entorno

Este documento describe cómo configurar las variables de entorno para la aplicación de escritorio.

## Crear archivo .env

Crea un archivo `.env` en el directorio `app_escritorio` con el siguiente contenido:

```
# Base de datos
DB_NAME=appwebmercado
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# API
API_BASE_URL=http://localhost:8000/api
API_TIMEOUT=30

# Interfaz de usuario
UI_WINDOW_TITLE=Gestión de Tareas y Análisis de Mercado
UI_WINDOW_WIDTH=1200
UI_WINDOW_HEIGHT=800
UI_THEME=light

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_FILE=app.log

# Aplicación
APP_NAME=Gestor de Mercado Laboral
APP_VERSION=1.0.0
APP_AUTHOR=Khadim Bamba
APP_WINDOW_TITLE=Gestor de Mercado Laboral - CRUD
APP_WINDOW_WIDTH=1200
APP_WINDOW_HEIGHT=800
APP_THEME=light

# Scraping
SCRAPER_DELAY=2
SCRAPER_TIMEOUT=30
SCRAPER_MAX_RETRIES=3
SCRAPER_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36

# Exportación
EXPORT_DEFAULT_FORMAT=csv
EXPORT_SUPPORTED_FORMATS=csv,xlsx,json
EXPORT_PATH=exports

# Validación
VALIDATION_MAX_TITLE_LENGTH=200
VALIDATION_MAX_DESCRIPTION_LENGTH=1000
VALIDATION_MIN_SALARY=0
VALIDATION_MAX_SALARY=1000000
VALIDATION_DATE_FORMAT=%Y-%m-%d
```

## Variables de Entorno para Despliegue en Cloud

Para el despliegue en un proveedor cloud, asegúrate de modificar las siguientes variables:

```
# Base de datos
DB_HOST=[IP_DE_CLOUD_SQL]
DB_USER=appuser
DB_PASSWORD=[CONTRASEÑA_SEGURA]

# API
API_BASE_URL=http://[IP_DE_LA_API]/api

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/appwebmercado/app.log
```

## Notas Importantes

- Asegúrate de que el archivo `.env` no se incluya en el control de versiones (está en `.gitignore`).
- Para entornos de producción, utiliza contraseñas seguras y no las compartas.
- Si estás desplegando en un servidor sin interfaz gráfica, asegúrate de configurar correctamente la variable `DISPLAY` en el archivo de servicio. 