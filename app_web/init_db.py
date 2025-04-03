import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def init_database():
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='postgresql',
            host='localhost',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'gestion_tareas_db'")
        exists = cursor.fetchone()
        
        if not exists:
            print("Creando base de datos gestion_tareas_db...")
            cursor.execute('CREATE DATABASE gestion_tareas_db')
            print("Base de datos creada exitosamente!")
        else:
            print("La base de datos ya existe, continuando...")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        raise e

if __name__ == '__main__':
    init_database() 