from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging
import sys

# Añadir el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Base

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        # Configuración directa de la base de datos
        self.db_name = 'appwebmercado'
        self.db_user = 'postgres'
        self.db_password = 'postgres'
        self.db_host = 'localhost'
        self.db_port = '5432'
        
        # Crear la URL de conexión
        self.database_url = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        
        # Crear el motor de SQLAlchemy
        self.engine = create_engine(self.database_url)
        
        # Crear la sesión
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def init_db(self):
        """Inicializa la base de datos creando todas las tablas"""
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """Retorna una nueva sesión de base de datos"""
        return self.session

    def close(self):
        """
        Cierra la conexión a la base de datos.
        """
        try:
            self.session.close()
            logger.info("Conexión a la base de datos cerrada correctamente")
        except Exception as e:
            logger.error(f"Error al cerrar la conexión a la base de datos: {str(e)}")

    def commit(self):
        """
        Realiza commit de la transacción actual.
        """
        try:
            self.session.commit()
            logger.info("Transacción confirmada correctamente")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error al confirmar la transacción: {str(e)}")
            raise

    def rollback(self):
        """
        Realiza rollback de la transacción actual.
        """
        try:
            self.session.rollback()
            logger.info("Transacción revertida correctamente")
        except Exception as e:
            logger.error(f"Error al revertir la transacción: {str(e)}")

    def refresh(self, obj):
        """
        Actualiza un objeto desde la base de datos.
        """
        try:
            self.session.refresh(obj)
            logger.info(f"Objeto {obj.__class__.__name__} actualizado correctamente")
        except Exception as e:
            logger.error(f"Error al actualizar objeto: {str(e)}")
            raise

    def add(self, obj):
        """
        Añade un objeto a la sesión.
        """
        try:
            self.session.add(obj)
            logger.info(f"Objeto {obj.__class__.__name__} añadido a la sesión")
        except Exception as e:
            logger.error(f"Error al añadir objeto a la sesión: {str(e)}")
            raise

    def delete(self, obj):
        """
        Elimina un objeto de la sesión.
        """
        try:
            self.session.delete(obj)
            logger.info(f"Objeto {obj.__class__.__name__} eliminado de la sesión")
        except Exception as e:
            logger.error(f"Error al eliminar objeto de la sesión: {str(e)}")
            raise

    def query(self, model):
        """
        Crea una consulta para un modelo específico.
        """
        return self.session.query(model)

    def execute(self, query):
        """
        Ejecuta una consulta SQL.
        """
        try:
            result = self.session.execute(query)
            logger.info("Consulta SQL ejecutada correctamente")
            return result
        except Exception as e:
            logger.error(f"Error al ejecutar consulta SQL: {str(e)}")
            raise 