import os
import psycopg2
from dotenv import load_dotenv

def init_database():
    # Cargar variables de entorno
    load_dotenv()
    
    # Conectar a PostgreSQL
    conn = psycopg2.connect(
        dbname='postgres',
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    try:
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (os.getenv('DB_NAME'),))
        exists = cursor.fetchone()
        
        if not exists:
            # Crear la base de datos
            cursor.execute(f"CREATE DATABASE {os.getenv('DB_NAME')}")
            print(f"Base de datos {os.getenv('DB_NAME')} creada exitosamente.")
        
        # Conectar a la base de datos creada
        conn.close()
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        cursor = conn.cursor()
        
        # Crear tablas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_offers (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                company VARCHAR(200) NOT NULL,
                location VARCHAR(200) NOT NULL,
                min_salary INTEGER,
                max_salary INTEGER,
                job_type VARCHAR(50) NOT NULL,
                fuente VARCHAR(50) DEFAULT 'Manual',
                description TEXT,
                requirements TEXT,
                publication_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(title, company)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habilidades (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_offers_habilidades (
                job_offers_id INTEGER REFERENCES job_offers(id) ON DELETE CASCADE,
                habilidades_id INTEGER REFERENCES habilidades(id) ON DELETE CASCADE,
                PRIMARY KEY (job_offers_id, habilidades_id)
            )
        """)
        
        # Crear índices
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_job_offers_title ON job_offers(title)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_job_offers_company ON job_offers(company)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_job_offers_location ON job_offers(location)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_job_offers_job_type ON job_offers(job_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_job_offers_fuente ON job_offers(fuente)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_habilidades_nombre ON habilidades(nombre)")
        
        conn.commit()
        print("Tablas e índices creados exitosamente.")
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_database() 