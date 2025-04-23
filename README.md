# Plataforma de Gestión de Tareas y Análisis del Mercado Laboral

## Descripción

Esta plataforma combina la **gestión colaborativa de tareas** con el **análisis del mercado laboral**, integrando inteligencia artificial para ofrecer recomendaciones personalizadas y predicciones de tendencias. Desarrollada como parte de un proyecto académico, consta de dos componentes principales:

- **Aplicación Web (Django)**: Permite la gestión de usuarios, proyectos, tareas, y análisis del mercado laboral con datos extraídos de Tecnoempleo, InfoJobs y LinkedIn.
- **Aplicación de Escritorio (PyQt6)**: Proporciona un CRUD para gestionar registros en la base de datos, como ofertas de empleo, habilidades y usuarios.

El sistema es modular, utiliza una base de datos relacional optimizada (PostgreSQL), e incluye visualizaciones avanzadas, modelos de inteligencia artificial, y documentación completa. El código fuente está disponible en [https://github.com/KhadimBamba2601/appwebmercado](https://github.com/KhadimBamba2601/appwebmercado).

## Características Principales

### Autenticación y Roles
- Registro e inicio de sesión con Django Authentication.
- **Roles**:
  - **Administrador**: Gestiona usuarios, datos del mercado, y configura el sistema.
  - **Gestor de Proyectos**: Crea y asigna proyectos y tareas.
  - **Colaborador**: Completa tareas y recibe recomendaciones basadas en habilidades.
- Restricción de acceso mediante permisos personalizados.

### Gestión de Proyectos y Tareas
- Modelos para **Proyectos**, **Tareas**, y **Usuarios** con relaciones muchos-a-muchos.
- **CRUD completo** para proyectos y tareas, con:
  - Estados: Pendiente, En Progreso, Completada.
  - Fechas límite, prioridades, y etiquetas de habilidades (e.g., "Django", "Python").
  - Asignación de colaboradores y seguimiento de progreso.
- Sistema de comentarios para tareas.

### Análisis del Mercado Laboral
- **Extracción de datos** de ofertas de empleo desde:
  - Tecnoempleo, InfoJobs, y LinkedIn (usando APIs o web scraping con Scrapy/BeautifulSoup, respetando términos de uso).
  - Datos almacenados: título, empresa, ubicación, habilidades, salario, fecha de publicación, número de postulantes.
- **Funcionalidades**:
  - Importación manual o programada de datos (administradores).
  - Dashboard con tendencias: habilidades más demandadas, comparación por fuente, y análisis por región.
  - Visualización con gráficos interactivos (Chart.js).
  - Seguimiento del número de postulantes por oferta.

### Inteligencia Artificial
- **Recomendaciones**: Modelo de IA (scikit-learn) que sugiere tareas y habilidades a colaboradores según su perfil y tendencias del mercado.
- **Predicciones**: Modelo de regresión para estimar la demanda futura de habilidades basado en datos históricos.
- Resultados integrados en el dashboard con visualizaciones claras.

### Aplicación de Escritorio
- **CRUD completo** para gestionar:
  - Ofertas de empleo (título, empresa, habilidades, etc.).
  - Habilidades (crear, editar, eliminar).
  - Usuarios (perfiles y roles).
- Desarrollada con **PyQt6**, con conexión directa a la base de datos PostgreSQL.
- Interfaz intuitiva, validación de datos, y diseño responsivo.

### Componentes Modulares
- **Usuarios**: Gestión de autenticación y roles.
- **Proyectos**: Creación y seguimiento de proyectos/tareas.
- **Análisis del Mercado**: Extracción y visualización de datos laborales.
- **Motor de IA**: Recomendaciones y predicciones.
- **Datos Externos**: Integración con Tecnoempleo, InfoJobs, LinkedIn.
- Cada componente es una aplicación Django independiente, diseñada para ser reutilizable.

### Extras Implementados
- **API REST** (Django REST Framework): Expone datos de ofertas y recomendaciones.
- **Notificaciones**: Correos para tareas asignadas y nuevas tendencias de habilidades.
- **Scraper Avanzado**: Manejo de autenticación para LinkedIn (con Selenium, respetando términos de uso).

## Prerrequisitos

- **Git**: Para clonar el repositorio.
- **Python**: 3.10 recomendado (compatible con Django 4.x).
- **PostgreSQL**: 13 o superior.
- **Navegador**: Chrome/Chromium (para web scraping y aplicación web).
- **Sistema Operativo**: Windows, Linux, o macOS.

## Requisitos del Sistema

### Software
- Python 3.10
- PostgreSQL 13+
- Chrome/Chromium

### Dependencias
Ver `requirements.txt` para la lista completa. Principales dependencias:
- Django 4.x
- psycopg2 (adaptador PostgreSQL)
- Scrapy/BeautifulSoup (web scraping)
- scikit-learn (IA)
- Chart.js, Select2, Bootstrap (frontend)
- PyQt6 (aplicación de escritorio)

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/KhadimBamba2601/appwebmercado.git
   cd appwebmercado
   ```

2. **Crear y activar entorno virtual**:
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/Mac
   env\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos PostgreSQL**:
   - Crear una base de datos:
     ```sql
     CREATE DATABASE appwebmercado;
     ```
   - Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:
     ```
     DB_NAME=appwebmercado
     DB_USER=tu_usuario
     DB_PASSWORD=tu_contraseña
     DB_HOST=localhost
     DB_PORT=5432
     SECRET_KEY=tu_clave_secreta_django
     EMAIL_HOST_USER=tu_email
     EMAIL_HOST_PASSWORD=tu_contraseña_email
     ```
   - **Nota**: Genera una `SECRET_KEY` segura para Django (puedes usar generadores online) y configura credenciales de correo (e.g., Gmail SMTP) para notificaciones.

5. **Aplicar migraciones**:
   ```bash
   cd app_web
   python manage.py migrate
   ```

6. **Crear superusuario (Administrador)**:
   ```bash
   python manage.py createsuperuser
   ```

7. **(Opcional) Cargar datos iniciales**:
   - Importar datos de prueba:
     ```bash
     python manage.py loaddata initial_data.json
     ```

## Uso

### Aplicación Web
1. Iniciar el servidor Django:
   ```bash
   cd app_web
   python manage.py runserver
   ```
2. Acceder a `http://localhost:8000` en un navegador.
3. Iniciar sesión como Administrador, Gestor de Proyectos, o Colaborador.
4. Usar el dashboard para:
   - Gestionar proyectos y tareas.
   - Analizar tendencias del mercado laboral.
   - Ver recomendaciones y predicciones de IA.

### Aplicación de Escritorio
1. Ejecutar la aplicación:
   ```bash
   cd app_escritorio
   python main.py
   ```
2. Conectar a la base de datos usando las credenciales del archivo `.env`.
3. Usar la interfaz para crear, leer, actualizar, o eliminar registros (ofertas, habilidades, usuarios).

## Estructura del Proyecto

```
appwebmercado/
├── app_web/                    # Aplicación Django
│   ├── usuarios/              # Gestión de autenticación y roles
│   ├── proyectos/             # Gestión de proyectos y tareas
│   ├── analisis_mercado/      # Extracción y análisis de datos laborales
│   ├── motor_ia/              # Modelos de recomendación y predicción
│   ├── datos_externos/        # Web scraping y APIs externas
│   ├── templates/             # Plantillas Django
│   ├── static/                # Archivos CSS, JS, imágenes
│   └── settings.py            # Configuración de Django
├── app_escritorio/            # Aplicación PyQt6
│   ├── main.py                # Entrada principal
│   ├── crud/                  # Componentes CRUD
│   └── ui/                    # Archivos de diseño UI
├── docs/                      # Documentación
│   ├── tecnica.pdf            # Documentación técnica
│   ├── manual_usuario.pdf     # Manual de usuario
│   └── pruebas.pdf            # Reporte de pruebas
├── requirements.txt           # Dependencias Python
├── LICENSE                    # Licencia MIT
└── README.md                  # Este archivo
```

## Base de Datos

- **Esquema**: Relacional, con modelos para `Usuario`, `Proyecto`, `Tarea`, `OfertaEmpleo`, `Habilidad`, y `DatosMercado`.
- **Relaciones**:
  - `OfertaEmpleo` ↔ `Habilidad` (muchos-a-muchos).
  - `Proyecto` → `Tarea` → `Usuario` (muchos-a-uno).
- **Índices**: Creados para consultas frecuentes (e.g., `fecha_publicacion`, `fuente`).
- **Diagrama ER**: Incluido en `docs/tecnica.pdf`.

## Pruebas

El proyecto incluye un conjunto de pruebas para garantizar su funcionalidad:
- **Pruebas unitarias**: Para vistas, modelos, y funciones de IA (`app_web/tests/`).
- **Pruebas de integración**: Flujos completos (e.g., crear tarea, importar datos).
- **Pruebas de frontend**: Validación de gráficos y formularios con Selenium.
- **Pruebas de usabilidad**: Evaluación con usuarios simulados.

Reporte completo en `docs/pruebas.pdf`.

## Documentación

1. **Documentación Técnica** (`docs/tecnica.pdf`):
   - Arquitectura del sistema (web y escritorio).
   - Diagrama ER de la base de datos.
   - Detalle de componentes modulares.
   - Implementación del modelo de IA (scikit-learn).
   - Instrucciones de instalación y configuración.

2. **Manual de Usuario** (`docs/manual_usuario.pdf`):
   - Guía para usar la aplicación web (login, gestión de tareas, análisis).
   - Instrucciones para la aplicación de escritorio (CRUD).
   - Capturas de pantalla y ejemplos.

3. **Video Demostrativo**:
   - Disponible en el repositorio (`docs/demo.mp4`).
   - Muestra el funcionamiento de la aplicación web, el CRUD de escritorio, y los análisis de datos (5-10 minutos).

## Problemas y Mejoras Futuras

### Problemas Identificados
- **Rendimiento del scraping**: La extracción de datos puede ser lenta con grandes volúmenes. Mitigado con programación asíncrona, pero requiere monitoreo.
- **Escalabilidad de IA**: Los modelos de IA actuales son básicos y podrían no escalar con datasets masivos.
- **Dependencias externas**: Los CDNs (Chart.js, Select2) pueden fallar en entornos sin conexión.

### Mejoras Propuestas
- Implementar caching para consultas frecuentes al mercado laboral.
- Desarrollar modelos de IA más avanzados (e.g., redes neuronales).
- Agregar soporte para internacionalización (i18n).
- Mejorar la accesibilidad de los gráficos con tablas de datos alternativas.

## Licencia

Este proyecto está licenciado bajo la **Licencia MIT**. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para consultas, sugerencias, o reportes de errores, contactar a:
- **Khadim Bamba**: [khim.2601@gmail.com]
- **Repositorio**: [https://github.com/KhadimBamba2601/appwebmercado](https://github.com/KhadimBamba2601/appwebmercado)

## Contribuciones

¡Las contribuciones son bienvenidas! Sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios y haz commit (`git commit -m "Añadir nueva funcionalidad"`).
4. Envía un pull request.

## Notas

- Si encuentras problemas durante la instalación, verifica las credenciales de PostgreSQL y asegúrate de que el servidor esté en ejecución.
- Para soporte adicional, abre un issue en el repositorio o contacta al desarrollador.