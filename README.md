# Plataforma de Gestión de Tareas y Análisis del Mercado Laboral

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/Documentation-ReadTheDocs-blue.svg)](https://appwebmercado.readthedocs.io/)

## 📋 Descripción
Esta plataforma web integra la gestión de tareas con el análisis del mercado laboral, permitiendo a los usuarios gestionar proyectos y tareas mientras obtienen insights valiosos sobre las tendencias del mercado laboral en el sector tecnológico. El sistema utiliza inteligencia artificial para proporcionar recomendaciones personalizadas y predicciones de tendencias del mercado.

## ✨ Características Principales
- 👥 **Gestión de usuarios y roles** (Administrador, Gestor de Proyectos, Colaborador)
- 📊 **Gestión de proyectos y tareas** con seguimiento de progreso
- 🔍 **Extracción y análisis de datos** de ofertas de empleo de múltiples fuentes
- 🤖 **Motor de IA** para recomendaciones y predicciones de tendencias
- 📱 **Interfaz web responsive** con diseño moderno
- 🔌 **API REST** para integración con otras aplicaciones
- 🖥️ **Aplicación de escritorio** para gestión directa de datos

## 🛠️ Requisitos del Sistema
- Python 3.8+
- Django 4.2+
- PostgreSQL 12+
- Node.js 14+ (para el frontend)
- Chrome/Chromium (para web scraping)

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/appwebmercado.git
cd appwebmercado
```

### 2. Crear y activar entorno virtual
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 5. Inicializar la base de datos
```bash
python manage.py migrate
python manage.py init_db
```

### 6. Crear superusuario
```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor de desarrollo
```bash
python manage.py runserver
```

## 📁 Estructura del Proyecto
```
appwebmercado/
├── app_web/                 # Aplicación principal Django
│   ├── api/                # API REST
│   ├── datos_externos/     # Scrapers y procesamiento de datos
│   ├── motor_ia/          # Motor de IA
│   ├── templates/         # Plantillas HTML
│   └── tests/            # Pruebas
├── app_escritorio/         # Aplicación de escritorio PyQt6
│   ├── crud/              # Componentes CRUD
│   ├── ui/                # Interfaz de usuario
│   └── main.py            # Punto de entrada
├── static/                # Archivos estáticos
├── media/                 # Archivos multimedia
└── docs/                  # Documentación
    ├── manual_usuario.md  # Manual de usuario
    └── documentacion_tecnica.md # Documentación técnica
```

## 📚 Documentación
- [Manual de Usuario](docs/manual_usuario.md)
- [Documentación Técnica](docs/documentacion_tecnica.md)
- [Guía de API](docs/api_guide.md)
- [Guía de Contribución](docs/contributing.md)

## 💻 Uso

### Gestión de Usuarios
- Los administradores pueden crear y gestionar usuarios
- Asignación de roles y permisos
- Gestión de perfiles de usuario

### Gestión de Proyectos
- Crear y asignar proyectos
- Gestionar tareas y subtareas
- Seguimiento de progreso
- Asignación de habilidades requeridas

### Análisis del Mercado
- Extracción automática de ofertas de empleo
- Análisis de tendencias
- Recomendaciones personalizadas
- Predicciones de mercado

## 🧪 Desarrollo

### Ejecutar Pruebas
```bash
python manage.py test
```

### Generar Documentación
```bash
cd docs
make html
```

### Contribuir
1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Contacto
Tu Nombre - [@tutwitter](https://twitter.com/tutwitter) - email@ejemplo.com

Link del Proyecto: [https://github.com/tu-usuario/appwebmercado](https://github.com/tu-usuario/appwebmercado)