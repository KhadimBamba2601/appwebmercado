# Guía de Contribución

## Introducción

¡Gracias por tu interés en contribuir a la Plataforma de Gestión de Tareas y Análisis del Mercado Laboral! Este documento proporciona las pautas y el proceso para contribuir al proyecto.

## Código de Conducta

Al participar en este proyecto, aceptas cumplir con nuestro [Código de Conducta](CODE_OF_CONDUCT.md). Por favor, léelo antes de contribuir.

## Proceso de Contribución

### 1. Reportar Problemas

Antes de crear un nuevo issue, por favor:

- Verifica que el problema no haya sido reportado ya
- Usa la plantilla de issue proporcionada
- Incluye información detallada sobre el problema:
  - Descripción clara
  - Pasos para reproducir
  - Comportamiento esperado vs. actual
  - Capturas de pantalla (si aplica)
  - Entorno (sistema operativo, versión de Python, etc.)

### 2. Proponer Mejoras

Si tienes una idea para mejorar el proyecto:

- Verifica que la mejora no haya sido propuesta ya
- Usa la plantilla de feature request
- Explica claramente el problema que resuelve o la mejora que aporta
- Incluye ejemplos de uso si es posible

### 3. Contribuir Código

#### Configuración del Entorno de Desarrollo

1. Haz un fork del repositorio
2. Clona tu fork:
   ```bash
   git clone https://github.com/tu-usuario/appwebmercado.git
   cd appwebmercado
   ```
3. Crea un entorno virtual:
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/Mac
   env\Scripts\activate     # Windows
   ```
4. Instala las dependencias de desarrollo:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
5. Configura pre-commit hooks:
   ```bash
   pre-commit install
   ```

#### Flujo de Trabajo Git

1. Asegúrate de que tu fork esté actualizado:
   ```bash
   git remote add upstream https://github.com/original/appwebmercado.git
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. Crea una rama para tu contribución:
   ```bash
   git checkout -b feature/nombre-de-tu-feature
   # o
   git checkout -b fix/nombre-de-tu-fix
   ```

3. Realiza tus cambios, siguiendo las pautas de código

4. Haz commit de tus cambios:
   ```bash
   git add .
   git commit -m "Descripción clara y concisa de los cambios"
   ```

5. Sube tus cambios a tu fork:
   ```bash
   git push origin feature/nombre-de-tu-feature
   ```

6. Abre un Pull Request (PR) desde tu fork al repositorio principal

#### Convenciones de Código

- **Estilo de código**: Seguimos [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- **Docstrings**: Usamos el formato de Google para docstrings
- **Tipado**: Usamos type hints de Python 3.8+
- **Tests**: Escribe tests para todo el código nuevo
- **Mensajes de commit**: Usa el formato [Conventional Commits](https://www.conventionalcommits.org/)

Ejemplo de docstring:

```python
def calcular_tendencia(datos: List[float], ventana: int = 7) -> float:
    """Calcula la tendencia de una serie de datos.
    
    Args:
        datos: Lista de valores numéricos.
        ventana: Tamaño de la ventana para el cálculo (por defecto: 7).
        
    Returns:
        float: Valor de la tendencia calculada.
        
    Raises:
        ValueError: Si la lista está vacía o la ventana es mayor que la longitud de datos.
    """
    # Implementación...
```

#### Estructura de Tests

- Los tests deben estar en el directorio `tests/` de cada aplicación
- Usa pytest para escribir tests
- Incluye tests unitarios y de integración
- Mantén una cobertura de código superior al 80%

Ejemplo de test:

```python
def test_calcular_tendencia():
    datos = [1.0, 2.0, 3.0, 4.0, 5.0]
    resultado = calcular_tendencia(datos, ventana=3)
    assert resultado == 1.0  # Tendencia esperada
```

### 4. Documentación

- Actualiza la documentación cuando sea necesario
- Sigue el formato Markdown para archivos .md
- Incluye ejemplos de código cuando sea apropiado
- Actualiza el README.md si introduces cambios significativos

### 5. Review de Código

- Los PR serán revisados por al menos un mantenedor
- Responde a los comentarios y sugerencias
- Realiza los cambios solicitados o explica por qué no son necesarios
- Mantén la discusión enfocada en el código

## Estructura del Proyecto

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
├── docs/                  # Documentación
├── requirements.txt       # Dependencias principales
├── requirements-dev.txt   # Dependencias de desarrollo
└── setup.py              # Configuración de instalación
```

## Guías Específicas

### Contribuir a la API

- Sigue las convenciones de REST
- Documenta todos los endpoints
- Incluye ejemplos de uso
- Asegúrate de manejar errores adecuadamente

### Contribuir al Motor de IA

- Documenta los algoritmos utilizados
- Incluye métricas de rendimiento
- Proporciona ejemplos de uso
- Considera la escalabilidad

### Contribuir a la Aplicación de Escritorio

- Sigue las guías de diseño de PyQt6
- Mantén la consistencia con la interfaz existente
- Asegúrate de que funcione en diferentes sistemas operativos
- Incluye capturas de pantalla en la documentación

## Reconocimiento

Las contribuciones serán reconocidas en:

- El archivo [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Los release notes de cada versión
- La documentación del proyecto

## Preguntas Frecuentes

### ¿Cómo puedo empezar si soy nuevo en el proyecto?

Recomendamos comenzar con:

1. Revisar los issues etiquetados como "good first issue"
2. Leer la documentación técnica
3. Configurar el entorno de desarrollo
4. Hacer pequeñas contribuciones para familiarizarte con el código

### ¿Qué hago si tengo preguntas?

- Abre un issue con la etiqueta "question"
- Pregunta en el canal de Discord del proyecto
- Contacta a los mantenedores por email

### ¿Cómo puedo convertirme en mantenedor?

Los mantenedores son seleccionados basándose en:

- Contribuciones consistentes y de alta calidad
- Compromiso con el proyecto
- Habilidad para revisar código y guiar a otros
- Consenso de los mantenedores actuales

## Contacto

Si tienes preguntas sobre cómo contribuir, contacta a:
- Email: contribuir@ejemplo.com
- Discord: [Link al servidor]
- GitHub Discussions: [Link a las discusiones] 