import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import logging
from typing import List, Dict, Any, Optional, Tuple

class DatabaseManager:
    def __init__(self):
        # Cargar variables de entorno
        load_dotenv()
        
        # Configurar logging
        self.setup_logging()
        
        # Configurar parámetros de conexión
        self.connection_params = {
            'dbname': os.getenv('DB_NAME', 'appwebmercado'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'postgresql'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432')
        }
        
        # Establecer conexión
        self.connect()
    
    def setup_logging(self):
        """Configura el sistema de logging"""
        # Crear directorio de logs si no existe
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, 'app_escritorio.log')),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('DatabaseManager')
    
    def connect(self):
        """Establece la conexión con la base de datos"""
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            self.conn.autocommit = True
            self.logger.info("Conexión a la base de datos establecida correctamente")
        except Exception as e:
            self.logger.error(f"Error al conectar con la base de datos: {str(e)}")
            raise
    
    def close(self):
        """Cierra la conexión con la base de datos"""
        if hasattr(self, 'conn'):
            self.conn.close()
            self.logger.info("Conexión a la base de datos cerrada")
    
    def execute_query(self, query: str, params: Tuple = None) -> Optional[List[Dict[str, Any]]]:
        """
        Ejecuta una consulta SQL y retorna los resultados como una lista de diccionarios
        """
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if cur.description:  # Si la consulta retorna resultados
                    return cur.fetchall()
                return None
        except Exception as e:
            self.logger.error(f"Error al ejecutar consulta: {str(e)}\nQuery: {query}\nParams: {params}")
            raise
    
    def get_table_data(self, table: str, where: str = None, params: Tuple = None, order_by: str = None) -> List[Dict[str, Any]]:
        """
        Obtiene todos los registros de una tabla con filtros opcionales
        """
        query = f"SELECT * FROM {table}"
        if where:
            query += f" WHERE {where}"
        if order_by:
            query += f" ORDER BY {order_by}"
        
        return self.execute_query(query, params) or []
    
    def insert_data(self, table: str, data: Dict[str, Any], on_conflict: str = None) -> int:
        """
        Inserta un nuevo registro en la tabla y retorna el ID.
        Si se especifica on_conflict, se usa para manejar conflictos de clave única.
        """
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        
        if on_conflict:
            query += f" ON CONFLICT {on_conflict} DO UPDATE SET "
            update_parts = [f"{k} = EXCLUDED.{k}" for k in data.keys() if k not in on_conflict.split(',')]
            query += ', '.join(update_parts)
        
        query += " RETURNING id"
        
        result = self.execute_query(query, tuple(data.values()))
        return result[0]['id'] if result else None
    
    def update_data(self, table: str, data: Dict[str, Any], where: str, params: Tuple) -> int:
        """
        Actualiza registros en la tabla que coincidan con la condición where
        """
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where} RETURNING id"
        
        all_params = tuple(data.values()) + params
        result = self.execute_query(query, all_params)
        return len(result) if result else 0
    
    def delete_data(self, table: str, where: str, params: Tuple) -> int:
        """
        Elimina registros de la tabla que coincidan con la condición where
        """
        query = f"DELETE FROM {table} WHERE {where} RETURNING id"
        
        result = self.execute_query(query, params)
        return len(result) if result else 0
    
    def execute_many(self, query: str, params_list: List[tuple]) -> None:
        """Execute a query with multiple parameter sets"""
        try:
            with self.conn.cursor() as cur:
                cur.executemany(query, params_list)
            self.logger.info(f"Executed batch query with {len(params_list)} items")
        except Exception as e:
            self.logger.error(f"Batch query execution error: {str(e)}\nQuery: {query}")
            raise
    
    def get_table_columns(self, table_name: str) -> List[str]:
        """Get column names for a table"""
        query = """
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position;
        """
        try:
            columns = self.execute_query(query, (table_name,))
            return [col['column_name'] for col in columns]
        except Exception as e:
            self.logger.error(f"Error getting table columns: {str(e)}")
            raise
    
    def begin_transaction(self):
        """Start a transaction"""
        self.conn.autocommit = False
    
    def commit_transaction(self):
        """Commit the current transaction"""
        self.conn.commit()
        self.conn.autocommit = True
    
    def rollback_transaction(self):
        """Rollback the current transaction"""
        self.conn.rollback()
        self.conn.autocommit = True 