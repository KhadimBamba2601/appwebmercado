import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def database_exists(cur, dbname):
    """Verifica si la base de datos existe."""
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (dbname,))
    return cur.fetchone() is not None

def create_database():
    """Create the database if it doesn't exist."""
    dbname = 'gestion_tareas_db'
    try:
        # Conectar a PostgreSQL usando la base de datos postgres por defecto
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='postgresql',
            host='localhost',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Verificar si la base de datos existe
        if not database_exists(cur, dbname):
            print(f"Creando base de datos '{dbname}'...")
            cur.execute(f'CREATE DATABASE {dbname}')
            print(f"Base de datos '{dbname}' creada exitosamente.")
        else:
            print(f"La base de datos '{dbname}' ya existe.")
            
        cur.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"Error de conexión a PostgreSQL: {e}")
        print("Asegúrate de que PostgreSQL esté instalado y ejecutándose.")
        return False
    except psycopg2.Error as e:
        print(f"Error al crear la base de datos: {e}")
        return False
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    success = create_database()
    if not success:
        sys.exit(1) 