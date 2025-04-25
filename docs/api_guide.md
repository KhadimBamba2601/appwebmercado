# Guía de API

## Introducción

Esta guía documenta la API REST de la Plataforma de Gestión de Tareas y Análisis del Mercado Laboral. La API permite a los desarrolladores integrar la funcionalidad de la plataforma en sus propias aplicaciones.

## Autenticación

La API utiliza autenticación basada en tokens JWT (JSON Web Tokens). Para obtener un token, debes hacer una solicitud POST a `/api/auth/login/` con tus credenciales.

```bash
curl -X POST https://api.ejemplo.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "contraseña"}'
```

La respuesta incluirá un token JWT que debes incluir en todas las solicitudes posteriores:

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

Para usar el token, inclúyelo en el encabezado `Authorization`:

```bash
curl -X GET https://api.ejemplo.com/api/proyectos/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

## Endpoints

### Autenticación

#### Login
- **URL**: `/api/auth/login/`
- **Método**: `POST`
- **Descripción**: Obtiene un token JWT para autenticación
- **Parámetros**:
  - `username`: Nombre de usuario
  - `password`: Contraseña
- **Respuesta**: Token JWT y token de actualización

#### Registro
- **URL**: `/api/auth/register/`
- **Método**: `POST`
- **Descripción**: Registra un nuevo usuario
- **Parámetros**:
  - `username`: Nombre de usuario
  - `email`: Correo electrónico
  - `password`: Contraseña
  - `rol`: Rol del usuario (ADMIN, GESTOR, COLAB)
- **Respuesta**: Datos del usuario creado

### Usuarios

#### Obtener Perfil
- **URL**: `/api/usuarios/profile/`
- **Método**: `GET`
- **Descripción**: Obtiene el perfil del usuario autenticado
- **Respuesta**: Datos del perfil del usuario

#### Actualizar Perfil
- **URL**: `/api/usuarios/profile/`
- **Método**: `PUT`
- **Descripción**: Actualiza el perfil del usuario autenticado
- **Parámetros**:
  - `nombre`: Nombre completo
  - `email`: Correo electrónico
  - `telefono`: Número de teléfono
  - `habilidades`: Lista de IDs de habilidades
- **Respuesta**: Perfil actualizado

#### Listar Usuarios (Admin)
- **URL**: `/api/usuarios/`
- **Método**: `GET`
- **Descripción**: Lista todos los usuarios (solo para administradores)
- **Parámetros de consulta**:
  - `rol`: Filtrar por rol
  - `search`: Buscar por nombre o email
- **Respuesta**: Lista de usuarios

### Proyectos

#### Listar Proyectos
- **URL**: `/api/proyectos/`
- **Método**: `GET`
- **Descripción**: Lista los proyectos del usuario
- **Parámetros de consulta**:
  - `estado`: Filtrar por estado (PEND, PROG, COMP)
  - `search`: Buscar por título
- **Respuesta**: Lista de proyectos

#### Obtener Proyecto
- **URL**: `/api/proyectos/{id}/`
- **Método**: `GET`
- **Descripción**: Obtiene los detalles de un proyecto
- **Respuesta**: Detalles del proyecto

#### Crear Proyecto
- **URL**: `/api/proyectos/`
- **Método**: `POST`
- **Descripción**: Crea un nuevo proyecto
- **Parámetros**:
  - `titulo`: Título del proyecto
  - `descripcion`: Descripción del proyecto
  - `fecha_inicio`: Fecha de inicio (YYYY-MM-DD)
  - `fecha_fin_estimada`: Fecha de fin estimada (YYYY-MM-DD)
  - `colaboradores`: Lista de IDs de usuarios
  - `habilidades_requeridas`: Lista de IDs de habilidades
- **Respuesta**: Proyecto creado

#### Actualizar Proyecto
- **URL**: `/api/proyectos/{id}/`
- **Método**: `PUT`
- **Descripción**: Actualiza un proyecto existente
- **Parámetros**: Mismos que en la creación
- **Respuesta**: Proyecto actualizado

#### Eliminar Proyecto
- **URL**: `/api/proyectos/{id}/`
- **Método**: `DELETE`
- **Descripción**: Elimina un proyecto
- **Respuesta**: Confirmación de eliminación

### Tareas

#### Listar Tareas
- **URL**: `/api/proyectos/{proyecto_id}/tareas/`
- **Método**: `GET`
- **Descripción**: Lista las tareas de un proyecto
- **Parámetros de consulta**:
  - `estado`: Filtrar por estado (PEND, PROG, COMP)
  - `asignado_a`: Filtrar por usuario asignado
- **Respuesta**: Lista de tareas

#### Obtener Tarea
- **URL**: `/api/tareas/{id}/`
- **Método**: `GET`
- **Descripción**: Obtiene los detalles de una tarea
- **Respuesta**: Detalles de la tarea

#### Crear Tarea
- **URL**: `/api/proyectos/{proyecto_id}/tareas/`
- **Método**: `POST`
- **Descripción**: Crea una nueva tarea
- **Parámetros**:
  - `titulo`: Título de la tarea
  - `descripcion`: Descripción de la tarea
  - `estado`: Estado inicial (PEND, PROG, COMP)
  - `prioridad`: Prioridad (BAJA, MEDIA, ALTA, URGENTE)
  - `fecha_fin_estimada`: Fecha de fin estimada (YYYY-MM-DD)
  - `asignado_a`: ID del usuario asignado
  - `habilidades_requeridas`: Lista de IDs de habilidades
- **Respuesta**: Tarea creada

#### Actualizar Tarea
- **URL**: `/api/tareas/{id}/`
- **Método**: `PUT`
- **Descripción**: Actualiza una tarea existente
- **Parámetros**: Mismos que en la creación
- **Respuesta**: Tarea actualizada

#### Eliminar Tarea
- **URL**: `/api/tareas/{id}/`
- **Método**: `DELETE`
- **Descripción**: Elimina una tarea
- **Respuesta**: Confirmación de eliminación

### Análisis del Mercado

#### Listar Ofertas de Empleo
- **URL**: `/api/analisis/ofertas/`
- **Método**: `GET`
- **Descripción**: Lista ofertas de empleo
- **Parámetros de consulta**:
  - `habilidad`: Filtrar por habilidad
  - `ubicacion`: Filtrar por ubicación
  - `fuente`: Filtrar por fuente (TECNO, INFO, LINK)
  - `fecha_desde`: Filtrar por fecha desde (YYYY-MM-DD)
  - `fecha_hasta`: Filtrar por fecha hasta (YYYY-MM-DD)
- **Respuesta**: Lista de ofertas de empleo

#### Obtener Oferta
- **URL**: `/api/analisis/ofertas/{id}/`
- **Método**: `GET`
- **Descripción**: Obtiene los detalles de una oferta
- **Respuesta**: Detalles de la oferta

#### Obtener Tendencias
- **URL**: `/api/analisis/tendencias/`
- **Método**: `GET`
- **Descripción**: Obtiene tendencias del mercado
- **Parámetros de consulta**:
  - `habilidad`: Filtrar por habilidad
  - `periodo`: Período de análisis (7d, 30d, 90d, 1y)
- **Respuesta**: Datos de tendencias

#### Obtener Predicciones
- **URL**: `/api/analisis/predicciones/`
- **Método**: `GET`
- **Descripción**: Obtiene predicciones de demanda
- **Parámetros de consulta**:
  - `habilidad`: Filtrar por habilidad
  - `horizonte`: Horizonte de predicción (30d, 90d, 180d)
- **Respuesta**: Predicciones de demanda

### Inteligencia Artificial

#### Obtener Recomendaciones
- **URL**: `/api/ia/recomendaciones/`
- **Método**: `GET`
- **Descripción**: Obtiene recomendaciones personalizadas
- **Parámetros de consulta**:
  - `tipo`: Tipo de recomendación (tarea, oferta, habilidad)
  - `limit`: Número máximo de recomendaciones
- **Respuesta**: Lista de recomendaciones

## Códigos de Estado

- `200 OK`: Solicitud exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Solicitud incorrecta
- `401 Unauthorized`: No autenticado
- `403 Forbidden`: No autorizado
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## Paginación

Los endpoints que devuelven listas utilizan paginación. Los parámetros de consulta son:

- `page`: Número de página (por defecto: 1)
- `page_size`: Tamaño de página (por defecto: 10, máximo: 100)

La respuesta incluye metadatos de paginación:

```json
{
  "count": 100,
  "next": "https://api.ejemplo.com/api/proyectos/?page=3",
  "previous": "https://api.ejemplo.com/api/proyectos/?page=1",
  "results": [...]
}
```

## Filtrado

Muchos endpoints soportan filtrado mediante parámetros de consulta. Por ejemplo:

```
GET /api/proyectos/?estado=PEND&search=web
```

## Ordenamiento

El ordenamiento se especifica mediante el parámetro `ordering`:

```
GET /api/proyectos/?ordering=-fecha_creacion
```

El prefijo `-` indica orden descendente.

## Ejemplos

### Crear un proyecto y asignar tareas

```bash
# 1. Obtener token
TOKEN=$(curl -X POST https://api.ejemplo.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "contraseña"}' | jq -r '.token')

# 2. Crear proyecto
PROJECT_ID=$(curl -X POST https://api.ejemplo.com/api/proyectos/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Proyecto Web",
    "descripcion": "Desarrollo de sitio web corporativo",
    "fecha_inicio": "2023-01-01",
    "fecha_fin_estimada": "2023-03-31",
    "colaboradores": [1, 2],
    "habilidades_requeridas": [5, 6, 7]
  }' | jq -r '.id')

# 3. Crear tarea
curl -X POST https://api.ejemplo.com/api/proyectos/$PROJECT_ID/tareas/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Diseño de interfaz",
    "descripcion": "Crear mockups de la interfaz de usuario",
    "estado": "PEND",
    "prioridad": "ALTA",
    "fecha_fin_estimada": "2023-01-15",
    "asignado_a": 1,
    "habilidades_requeridas": [5, 8]
  }'
```

## Limitaciones

- Máximo de 1000 solicitudes por hora por token
- Tamaño máximo de solicitud: 1MB
- Tiempo máximo de respuesta: 30 segundos

## Soporte

Para soporte técnico o consultas sobre la API, contacta a:
- Email: api@ejemplo.com
- Documentación: https://api.ejemplo.com/docs/ 