from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios_usuario'

    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True)
    email = Column(String(254), unique=True)
    rol = Column(String(20))
    fecha_nacimiento = Column(DateTime, nullable=True)
    telefono = Column(String(15), nullable=True)
    foto_perfil = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime, default=datetime.now)

    # Relaciones
    proyectos_gestionados = relationship("Proyecto", back_populates="gestor")
    proyectos_colaboracion = relationship("Proyecto", secondary="proyectos_proyecto_colaboradores")
    tareas_asignadas = relationship("Tarea", back_populates="asignado_a")
    habilidades = relationship("Habilidad", secondary="usuarios_usuario_habilidades")

class Habilidad(Base):
    __tablename__ = 'usuarios_habilidad'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True)
    descripcion = Column(Text, nullable=True)
    categoria = Column(String(50), nullable=True)

class Proyecto(Base):
    __tablename__ = 'proyectos_proyecto'

    id = Column(Integer, primary_key=True)
    titulo = Column(String(200))
    descripcion = Column(Text)
    fecha_inicio = Column(DateTime)
    fecha_fin_estimada = Column(DateTime)
    fecha_fin_real = Column(DateTime, nullable=True)
    estado = Column(String(10))
    gestor_id = Column(Integer, ForeignKey('usuarios_usuario.id'))
    fecha_creacion = Column(DateTime, default=datetime.now)
    ultima_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relaciones
    gestor = relationship("Usuario", back_populates="proyectos_gestionados")
    colaboradores = relationship("Usuario", secondary="proyectos_proyecto_colaboradores")
    tareas = relationship("Tarea", back_populates="proyecto")
    habilidades_requeridas = relationship("Habilidad", secondary="proyectos_proyecto_habilidades_requeridas")

class Tarea(Base):
    __tablename__ = 'proyectos_tarea'

    id = Column(Integer, primary_key=True)
    titulo = Column(String(200))
    descripcion = Column(Text)
    proyecto_id = Column(Integer, ForeignKey('proyectos_proyecto.id'))
    asignado_a_id = Column(Integer, ForeignKey('usuarios_usuario.id'), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.now)
    fecha_limite = Column(DateTime)
    fecha_completada = Column(DateTime, nullable=True)
    prioridad = Column(String(10))
    estado = Column(String(10))
    fecha_fin_estimada = Column(DateTime)
    fecha_fin_real = Column(DateTime, nullable=True)
    ultima_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relaciones
    proyecto = relationship("Proyecto", back_populates="tareas")
    asignado_a = relationship("Usuario", back_populates="tareas_asignadas")
    habilidades_requeridas = relationship("Habilidad", secondary="proyectos_tarea_habilidades_requeridas")

class OfertaEmpleo(Base):
    __tablename__ = 'analisis_mercado_ofertaempleo'

    id = Column(Integer, primary_key=True)
    titulo = Column(String(200))
    empresa = Column(String(200))
    descripcion = Column(Text)
    ubicacion = Column(String(200))
    salario_min = Column(Float, nullable=True)
    salario_max = Column(Float, nullable=True)
    tipo_contrato = Column(String(10))
    fecha_publicacion = Column(DateTime)
    fecha_vencimiento = Column(DateTime, nullable=True)
    url_original = Column(String(500))
    fuente_id = Column(Integer, ForeignKey('analisis_mercado_fuentedatos.id'))
    candidatos_inscritos = Column(Integer, default=0)
    activa = Column(Boolean, default=True)

    # Relaciones
    fuente = relationship("FuenteDatos")
    habilidades_requeridas = relationship("Habilidad", secondary="analisis_mercado_ofertaempleo_habilidades_requeridas")

class FuenteDatos(Base):
    __tablename__ = 'analisis_mercado_fuentedatos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True)
    url_base = Column(String(500))
    api_key = Column(String(200), nullable=True)
    activo = Column(Boolean, default=True)
    ultima_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class AnalisisMercado(Base):
    __tablename__ = 'analisis_mercado_analisismercado'

    id = Column(Integer, primary_key=True)
    fecha_analisis = Column(DateTime, default=datetime.now)
    periodo = Column(String(50))
    habilidades_mas_demandadas = Column(JSON)
    salarios_promedio = Column(JSON)
    tendencias_crecimiento = Column(JSON)
    regiones_mas_activas = Column(JSON)

class PrediccionMercado(Base):
    __tablename__ = 'analisis_mercado_prediccionmercado'

    id = Column(Integer, primary_key=True)
    fecha_prediccion = Column(DateTime, default=datetime.now)
    periodo_futuro = Column(String(50))
    habilidades_futuras = Column(JSON)
    salarios_estimados = Column(JSON)
    tendencias_predichas = Column(JSON)
    confianza_prediccion = Column(Float) 