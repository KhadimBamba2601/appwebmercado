import requests
from bs4 import BeautifulSoup
import re
import logging
from datetime import datetime
import psycopg2
from dotenv import load_dotenv
import os

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

# Patrón para extraer salarios
SALARY_PATTERN = re.compile(r'(\d{1,3}(?:\.\d{3})*)\s*€')

# Palabras clave para tipos de trabajo
JOB_TYPE_KEYWORDS = {
    'remoto': ['remoto', 'remote', 'teletrabajo', 'home office'],
    'presencial': ['presencial', 'oficina', 'in situ'],
    'híbrido': ['híbrido', 'hibrido', 'mixto', 'flexible']
}

def scrape_infojobs():
    """
    Scrapea ofertas de trabajo de InfoJobs
    """
    url = "https://www.infojobs.net/jobsearch/search-results/list.xhtml"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ofertas = []
        for oferta in soup.find_all('div', class_='ij-OfferCardContent'):
            try:
                titulo = oferta.find('h2', class_='ij-OfferCardContent-title').text.strip() if oferta.find('h2', class_='ij-OfferCardContent-title') else 'Sin título'
                empresa = oferta.find('span', class_='ij-OfferCardContent-companyName').text.strip() if oferta.find('span', class_='ij-OfferCardContent-companyName') else 'Empresa no especificada'
                ubicacion = oferta.find('span', class_='ij-OfferCardContent-location').text.strip() if oferta.find('span', class_='ij-OfferCardContent-location') else 'Ubicación no especificada'
                
                ofertas.append({
                    'titulo': titulo,
                    'empresa': empresa,
                    'ubicacion': ubicacion,
                    'fecha_publicacion': datetime.now().strftime('%Y-%m-%d'),
                    'salario_min': None,
                    'salario_max': None,
                    'tipo_trabajo': 'No especificado',
                    'descripcion': '',
                    'habilidades': [],
                    'fuente': 'InfoJobs'
                })
                
            except Exception as e:
                logging.error(f"Error procesando una oferta individual de InfoJobs: {str(e)}")
                continue
        
        return ofertas
    
    except requests.RequestException as e:
        logging.error(f"Error al hacer la petición HTTP a InfoJobs: {str(e)}")
        return []
    except Exception as e:
        logging.error(f"Error inesperado al scrapear InfoJobs: {str(e)}")
        return []

def scrape_linkedin():
    """
    Scrapea ofertas de trabajo de LinkedIn
    """
    url = "https://www.linkedin.com/jobs/search"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ofertas = []
        for oferta in soup.find_all('div', class_='base-card'):
            try:
                titulo = oferta.find('h3', class_='base-search-card__title').text.strip() if oferta.find('h3', class_='base-search-card__title') else 'Sin título'
                empresa = oferta.find('h4', class_='base-search-card__subtitle').text.strip() if oferta.find('h4', class_='base-search-card__subtitle') else 'Empresa no especificada'
                ubicacion = oferta.find('span', class_='job-search-card__location').text.strip() if oferta.find('span', class_='job-search-card__location') else 'Ubicación no especificada'
                
                ofertas.append({
                    'titulo': titulo,
                    'empresa': empresa,
                    'ubicacion': ubicacion,
                    'fecha_publicacion': datetime.now().strftime('%Y-%m-%d'),
                    'salario_min': None,
                    'salario_max': None,
                    'tipo_trabajo': 'No especificado',
                    'descripcion': '',
                    'habilidades': [],
                    'fuente': 'LinkedIn'
                })
                
            except Exception as e:
                logging.error(f"Error procesando una oferta individual de LinkedIn: {str(e)}")
                continue
        
        return ofertas
    
    except requests.RequestException as e:
        logging.error(f"Error al hacer la petición HTTP a LinkedIn: {str(e)}")
        return []
    except Exception as e:
        logging.error(f"Error inesperado al scrapear LinkedIn: {str(e)}")
        return []

def guardar_ofertas(ofertas, conn):
    """
    Guarda las ofertas en la base de datos
    """
    cursor = conn.cursor()
    
    for oferta in ofertas:
        try:
            # Insertar o actualizar oferta
            cursor.execute("""
                INSERT INTO job_offers (
                    title, company, location, publication_date,
                    min_salary, max_salary, job_type,
                    description, fuente
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (title, company) DO UPDATE SET
                    location = EXCLUDED.location,
                    publication_date = EXCLUDED.publication_date,
                    min_salary = EXCLUDED.min_salary,
                    max_salary = EXCLUDED.max_salary,
                    job_type = EXCLUDED.job_type,
                    description = EXCLUDED.description
                RETURNING id
            """, (
                oferta['titulo'],
                oferta['empresa'],
                oferta['ubicacion'],
                oferta['fecha_publicacion'],
                oferta['salario_min'],
                oferta['salario_max'],
                oferta['tipo_trabajo'],
                oferta['descripcion'],
                oferta['fuente']
            ))
            
            oferta_id = cursor.fetchone()[0]
            
            # Insertar habilidades
            for habilidad in oferta['habilidades']:
                # Insertar habilidad si no existe
                cursor.execute("""
                    INSERT INTO habilidades (nombre)
                    VALUES (%s)
                    ON CONFLICT (nombre) DO NOTHING
                    RETURNING id
                """, (habilidad,))
                
                habilidad_id = cursor.fetchone()
                if habilidad_id:
                    habilidad_id = habilidad_id[0]
                else:
                    cursor.execute("SELECT id FROM habilidades WHERE nombre = %s", (habilidad,))
                    habilidad_id = cursor.fetchone()[0]
                
                # Relacionar oferta con habilidad
                cursor.execute("""
                    INSERT INTO job_offers_habilidades (job_offers_id, habilidades_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                """, (oferta_id, habilidad_id))
            
            conn.commit()
            logging.info(f"Oferta guardada: {oferta['titulo']} - {oferta['empresa']}")
            
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al guardar oferta {oferta['titulo']}: {str(e)}")

def main():
    """
    Función principal que ejecuta el scraper
    """
    # Cargar variables de entorno
    load_dotenv()
    
    # Conectar a la base de datos
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        
        # Scrapear ofertas de diferentes fuentes
        todas_las_ofertas = []
        
        # InfoJobs
        ofertas_infojobs = scrape_infojobs()
        logging.info(f"Se encontraron {len(ofertas_infojobs)} ofertas en InfoJobs")
        todas_las_ofertas.extend(ofertas_infojobs)
        
        # LinkedIn
        ofertas_linkedin = scrape_linkedin()
        logging.info(f"Se encontraron {len(ofertas_linkedin)} ofertas en LinkedIn")
        todas_las_ofertas.extend(ofertas_linkedin)
        
        # Guardar todas las ofertas
        if todas_las_ofertas:
            guardar_ofertas(todas_las_ofertas, conn)
            logging.info(f"Se guardaron {len(todas_las_ofertas)} ofertas en total")
        else:
            logging.warning("No se encontraron ofertas en ninguna fuente")
        
        conn.close()
        logging.info("Proceso completado exitosamente")
        
    except Exception as e:
        logging.error(f"Error en el proceso principal: {str(e)}")

if __name__ == "__main__":
    main() 