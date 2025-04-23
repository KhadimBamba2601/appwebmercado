# datos_externos/scraper.py
from .tecnoempleo_scraper import scrape_tecnoempleo
from .linkedin_scraper import scrape_linkedin
from .infojobs_scraper import scrape_infojobs
from .utils import guardar_ofertas
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from analisis_mercado.models import OfertaEmpleo, Habilidad
from .utils import limpiar_ofertas_por_fuente, SALARIO_PATTERN, TIPO_TRABAJO_KEYWORDS

def scrape_tecnoempleo(titulo='', ubicacion=''):
    """
    Scrapes job offers from Tecnoempleo based on title and location.
    
    Args:
        titulo (str): Job title to search for
        ubicacion (str): Location to search in
        
    Returns:
        list: List of dictionaries containing job offers
    """
    base_url = "https://www.tecnoempleo.com"
    search_url = f"{base_url}/buscar-empleo.php"
    
    params = {
        'palabra': titulo,
        'donde': ubicacion,
        'orden': 'fecha'
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ofertas = []
        job_listings = soup.find_all('div', class_='job-item')
        
        for job in job_listings:
            try:
                # Extract job details
                titulo = job.find('h2').text.strip()
                empresa = job.find('span', class_='company').text.strip()
                ubicacion = job.find('span', class_='location').text.strip()
                fecha_text = job.find('span', class_='date').text.strip()
                fecha = datetime.strptime(fecha_text, '%d/%m/%Y').date()
                
                # Get job details page
                detail_url = base_url + job.find('a')['href']
                detail_response = requests.get(detail_url)
                detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                
                # Extract salary and job type
                descripcion = detail_soup.find('div', class_='job-description').text
                salario_match = SALARIO_PATTERN.search(descripcion)
                salario = salario_match.group(1) if salario_match else None
                
                # Determine job type
                tipo_trabajo = 'No especificado'
                for tipo, keywords in TIPO_TRABAJO_KEYWORDS.items():
                    if any(keyword.lower() in descripcion.lower() for keyword in keywords):
                        tipo_trabajo = tipo
                        break
                
                # Extract required skills
                habilidades = []
                skills_section = detail_soup.find('div', class_='skills')
                if skills_section:
                    skills = skills_section.find_all('span', class_='skill')
                    habilidades = [skill.text.strip() for skill in skills]
                
                oferta = {
                    'titulo': titulo,
                    'empresa': empresa,
                    'ubicacion': ubicacion,
                    'tipo_trabajo': tipo_trabajo,
                    'salario': salario,
                    'fuente': 'Tecnoempleo',
                    'fecha_publicacion': fecha,
                    'habilidades': habilidades,
                    'url': detail_url
                }
                
                ofertas.append(oferta)
                
            except Exception as e:
                print(f"Error procesando oferta: {str(e)}")
                continue
                
        return ofertas
        
    except Exception as e:
        print(f"Error al hacer scraping de Tecnoempleo: {str(e)}")
        return []

def guardar_ofertas(ofertas):
    """
    Saves job offers to the database.
    
    Args:
        ofertas (list): List of dictionaries containing job offers
    """
    for oferta in ofertas:
        try:
            # Create or update job offer
            obj, created = OfertaEmpleo.objects.update_or_create(
                titulo=oferta['titulo'],
                empresa=oferta['empresa'],
                defaults={
                    'ubicacion': oferta['ubicacion'],
                    'tipo_trabajo': oferta['tipo_trabajo'],
                    'salario': oferta['salario'],
                    'fuente': oferta['fuente'],
                    'fecha_publicacion': oferta['fecha_publicacion'],
                    'url': oferta['url']
                }
            )
            
            # Add skills
            for habilidad_nombre in oferta['habilidades']:
                habilidad, _ = Habilidad.objects.get_or_create(nombre=habilidad_nombre)
                obj.habilidades.add(habilidad)
                
        except Exception as e:
            print(f"Error guardando oferta: {str(e)}")
            continue

def main():
    try:
        # Scraping de Tecnoempleo
        ofertas_tecno = scrape_tecnoempleo(titulo="programador", ubicacion="Madrid")
        guardar_ofertas(ofertas_tecno)
        print(f"Guardadas {len(ofertas_tecno)} ofertas de Tecnoempleo.")
        
        # Scraping de LinkedIn
        ofertas_linkedin = scrape_linkedin(titulo="programador", ubicacion="Madrid")
        guardar_ofertas(ofertas_linkedin)
        print(f"Guardadas {len(ofertas_linkedin)} ofertas de LinkedIn.")
        
        # Scraping de InfoJobs
        ofertas_infojobs = scrape_infojobs(titulo="programador", ubicacion="Madrid")
        guardar_ofertas(ofertas_infojobs)
        print(f"Guardadas {len(ofertas_infojobs)} ofertas de InfoJobs.")
    except Exception as e:
        print(f"Error durante la ejecución: {e}")

if __name__ == "__main__":
    main()