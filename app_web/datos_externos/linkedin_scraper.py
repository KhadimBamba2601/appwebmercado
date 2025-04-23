# datos_externos/linkedin_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from analisis_mercado.models import OfertaEmpleo, Habilidad
from .utils import SALARIO_PATTERN, TIPO_TRABAJO_KEYWORDS

def scrape_linkedin(titulo='', ubicacion=''):
    """
    Scrapes job offers from LinkedIn based on title and location.
    
    Args:
        titulo (str): Job title to search for
        ubicacion (str): Location to search in
        
    Returns:
        list: List of dictionaries containing job offers
    """
    base_url = "https://www.linkedin.com"
    search_url = f"{base_url}/jobs/search"
    
    params = {
        'keywords': titulo,
        'location': ubicacion,
        'sortBy': 'DD'
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ofertas = []
        job_listings = soup.find_all('div', class_='job-card-container')
        
        for job in job_listings:
            try:
                # Extract job details
                titulo = job.find('h3', class_='base-search-card__title').text.strip()
                empresa = job.find('h4', class_='base-search-card__subtitle').text.strip()
                ubicacion = job.find('span', class_='job-search-card__location').text.strip()
                fecha_text = job.find('time')['datetime']
                fecha = datetime.strptime(fecha_text, '%Y-%m-%d').date()
                
                # Get job details page
                detail_url = base_url + job.find('a')['href']
                detail_response = requests.get(detail_url)
                detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                
                # Extract salary and job type
                descripcion = detail_soup.find('div', class_='description__text').text
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
                skills_section = detail_soup.find('div', class_='job-criteria__list')
                if skills_section:
                    skills = skills_section.find_all('span', class_='job-criteria__text')
                    habilidades = [skill.text.strip() for skill in skills]
                
                oferta = {
                    'titulo': titulo,
                    'empresa': empresa,
                    'ubicacion': ubicacion,
                    'tipo_trabajo': tipo_trabajo,
                    'salario': salario,
                    'fuente': 'LinkedIn',
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
        print(f"Error al hacer scraping de LinkedIn: {str(e)}")
        return []