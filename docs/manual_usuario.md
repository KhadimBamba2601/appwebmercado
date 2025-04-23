# Manual de Usuario

## Índice
1. [Introducción](#introducción)
2. [Acceso al Sistema](#acceso-al-sistema)
3. [Gestión de Usuarios](#gestión-de-usuarios)
4. [Gestión de Proyectos](#gestión-de-proyectos)
5. [Análisis del Mercado Laboral](#análisis-del-mercado-laboral)
6. [Aplicación de Escritorio](#aplicación-de-escritorio)

## Introducción

Este manual está diseñado para guiar a los usuarios en el uso de la Plataforma de Gestión de Tareas y Análisis del Mercado Laboral. La plataforma consta de dos componentes principales:

1. **Aplicación Web**: Para la gestión de usuarios, proyectos y análisis del mercado.
2. **Aplicación de Escritorio**: Para la gestión directa de datos.

## Acceso al Sistema

### Registro de Usuario
1. Acceder a `http://localhost:8000/register/`
2. Completar el formulario con:
   - Nombre de usuario
   - Correo electrónico
   - Contraseña
   - Rol (Administrador, Gestor de Proyectos o Colaborador)
3. Hacer clic en "Registrar"

### Inicio de Sesión
1. Acceder a `http://localhost:8000/login/`
2. Ingresar nombre de usuario y contraseña
3. Hacer clic en "Iniciar Sesión"

## Gestión de Usuarios

### Perfil de Usuario
- **Acceso**: Menú superior > Mi Perfil
- **Funcionalidades**:
  - Ver y editar información personal
  - Gestionar habilidades
  - Ver recomendaciones de ofertas

### Roles y Permisos
- **Administrador**:
  - Gestionar todos los usuarios
  - Configurar el sistema
  - Acceso total a datos
- **Gestor de Proyectos**:
  - Crear y gestionar proyectos
  - Asignar tareas
  - Ver análisis del mercado
- **Colaborador**:
  - Ver tareas asignadas
  - Actualizar estado de tareas
  - Ver recomendaciones

## Gestión de Proyectos

### Crear Proyecto
1. Acceder a "Proyectos" > "Nuevo Proyecto"
2. Completar información:
   - Nombre del proyecto
   - Descripción
   - Fechas de inicio y fin
   - Gestor asignado
3. Hacer clic en "Crear"

### Gestionar Tareas
1. **Crear Tarea**:
   - Seleccionar proyecto
   - Hacer clic en "Nueva Tarea"
   - Completar detalles:
     - Título
     - Descripción
     - Prioridad
     - Fecha límite
     - Colaboradores
     - Habilidades requeridas

2. **Actualizar Estado**:
   - Seleccionar tarea
   - Cambiar estado (Pendiente, En Progreso, Completada)
   - Agregar comentarios si es necesario

3. **Seguimiento**:
   - Ver progreso en dashboard
   - Revisar comentarios
   - Ver asignaciones

## Análisis del Mercado Laboral

### Dashboard
- **Acceso**: Menú principal > Dashboard
- **Funcionalidades**:
  - Ver tendencias del mercado
  - Analizar habilidades demandadas
  - Comparar fuentes de empleo
  - Ver predicciones

### Recomendaciones
- **Acceso**: Menú principal > Recomendaciones
- **Funcionalidades**:
  - Ver ofertas recomendadas
  - Filtrar por habilidades
  - Ver similitud con perfil
  - Guardar ofertas favoritas

### Búsqueda Avanzada
1. Acceder a "Análisis" > "Búsqueda"
2. Usar filtros:
   - Habilidades
   - Ubicación
   - Salario
   - Tipo de contrato
3. Ver resultados y estadísticas

## Aplicación de Escritorio

### Instalación
1. Asegurarse de tener Python 3.8+ instalado
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar la aplicación:
   ```bash
   python app_escritorio/main.py
   ```

### Gestión de Datos

#### Ofertas de Empleo
1. **Añadir Oferta**:
   - Hacer clic en "Nueva Oferta"
   - Completar formulario
   - Guardar cambios

2. **Editar Oferta**:
   - Seleccionar oferta
   - Hacer clic en "Editar"
   - Modificar datos
   - Guardar cambios

3. **Eliminar Oferta**:
   - Seleccionar oferta
   - Hacer clic en "Eliminar"
   - Confirmar acción

#### Habilidades
1. **Añadir Habilidad**:
   - Hacer clic en "Nueva Habilidad"
   - Ingresar nombre y categoría
   - Guardar cambios

2. **Editar Habilidad**:
   - Seleccionar habilidad
   - Modificar datos
   - Guardar cambios

#### Usuarios
1. **Añadir Usuario**:
   - Hacer clic en "Nuevo Usuario"
   - Completar información
   - Guardar cambios

2. **Editar Usuario**:
   - Seleccionar usuario
   - Modificar datos
   - Guardar cambios

## Consejos y Mejores Prácticas

### Seguridad
- Cambiar contraseña regularmente
- No compartir credenciales
- Cerrar sesión al terminar

### Productividad
- Usar etiquetas en tareas
- Mantener habilidades actualizadas
- Revisar recomendaciones regularmente

### Colaboración
- Comunicar cambios en tareas
- Usar sistema de comentarios
- Compartir hallazgos relevantes

## Solución de Problemas

### Problemas Comunes
1. **No puedo iniciar sesión**
   - Verificar credenciales
   - Usar recuperación de contraseña
   - Contactar al administrador

2. **No veo mis tareas**
   - Verificar filtros
   - Comprobar asignaciones
   - Actualizar página

3. **La aplicación de escritorio no inicia**
   - Verificar instalación de Python
   - Comprobar dependencias
   - Revisar conexión a base de datos

### Contacto de Soporte
- Email: soporte@ejemplo.com
- Teléfono: +XX XXX XXX XXX
- Horario: Lunes a Viernes, 9:00 - 18:00 