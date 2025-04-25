import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import re
from datetime import datetime

def scrape_tecnoempleo(titulo: str = '', ubicacion: str = '') -> List[Dict[str, Any]]:
    """
    Scrape ofertas de trabajo de Tecnoempleo
    """
    ofertas = []
    base_url = 'https://www.tecnoempleo.com'
    search_url = f'{base_url}/buscar-ofertas-trabajo'
    
    params = {}
    if titulo:
        params['q'] = titulo
    if ubicacion:
        params['l'] = ubicacion
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all('div', class_='job-card')
        
        for card in job_cards:
            try:
                title = card.find('h2', class_='job-title').text.strip()
                company = card.find('div', class_='company-name').text.strip()
                location = card.find('div', class_='location').text.strip()
                
                # Extraer salario si está disponible
                salary_text = card.find('div', class_='salary')
                min_salary = max_salary = 0
                if salary_text:
                    salary_match = re.search(r'(\d+)[kK]?\s*-\s*(\d+)[kK]?', salary_text.text)
                    if salary_match:
                        min_salary = int(salary_match.group(1)) * 1000
                        max_salary = int(salary_match.group(2)) * 1000
                
                # Extraer tipo de trabajo
                job_type = card.find('div', class_='job-type').text.strip()
                
                # Obtener descripción y requisitos
                job_url = base_url + card.find('a')['href']
                job_response = requests.get(job_url)
                job_soup = BeautifulSoup(job_response.text, 'html.parser')
                
                description = job_soup.find('div', class_='job-description').text.strip()
                requirements = job_soup.find('div', class_='job-requirements').text.strip()
                
                # Extraer habilidades de la descripción y requisitos
                habilidades = extract_habilidades(description + ' ' + requirements)
                
                oferta = {
                    'title': title,
                    'company': company,
                    'location': location,
                    'min_salary': min_salary,
                    'max_salary': max_salary,
                    'job_type': job_type,
                    'description': description,
                    'requirements': requirements,
                    'publication_date': datetime.now().strftime('%Y-%m-%d'),
                    'fuente': 'Tecnoempleo',
                    'habilidades': habilidades
                }
                
                ofertas.append(oferta)
                
            except Exception as e:
                print(f"Error al procesar oferta de Tecnoempleo: {str(e)}")
                continue
    
    except Exception as e:
        print(f"Error al scrapear Tecnoempleo: {str(e)}")
    
    return ofertas

def scrape_infojobs(titulo: str = '', ubicacion: str = '') -> List[Dict[str, Any]]:
    """
    Scrape ofertas de trabajo de InfoJobs
    """
    ofertas = []
    base_url = 'https://www.infojobs.net'
    search_url = f'{base_url}/jobsearch/search-results/list.xhtml'
    
    params = {}
    if titulo:
        params['keyword'] = titulo
    if ubicacion:
        params['provincia'] = ubicacion
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all('div', class_='ij-List-item')
        
        for card in job_cards:
            try:
                title = card.find('h2', class_='ij-List-item-title').text.strip()
                company = card.find('span', class_='ij-List-item-company').text.strip()
                location = card.find('span', class_='ij-List-item-location').text.strip()
                
                # Extraer salario si está disponible
                salary_text = card.find('span', class_='ij-List-item-salary')
                min_salary = max_salary = 0
                if salary_text:
                    salary_match = re.search(r'(\d+)[kK]?\s*-\s*(\d+)[kK]?', salary_text.text)
                    if salary_match:
                        min_salary = int(salary_match.group(1)) * 1000
                        max_salary = int(salary_match.group(2)) * 1000
                
                # Extraer tipo de trabajo
                job_type = card.find('span', class_='ij-List-item-contract').text.strip()
                
                # Obtener descripción y requisitos
                job_url = base_url + card.find('a')['href']
                job_response = requests.get(job_url)
                job_soup = BeautifulSoup(job_response.text, 'html.parser')
                
                description = job_soup.find('div', class_='ij-Offer-description').text.strip()
                requirements = job_soup.find('div', class_='ij-Offer-requirements').text.strip()
                
                # Extraer habilidades de la descripción y requisitos
                habilidades = extract_habilidades(description + ' ' + requirements)
                
                oferta = {
                    'title': title,
                    'company': company,
                    'location': location,
                    'min_salary': min_salary,
                    'max_salary': max_salary,
                    'job_type': job_type,
                    'description': description,
                    'requirements': requirements,
                    'publication_date': datetime.now().strftime('%Y-%m-%d'),
                    'fuente': 'InfoJobs',
                    'habilidades': habilidades
                }
                
                ofertas.append(oferta)
                
            except Exception as e:
                print(f"Error al procesar oferta de InfoJobs: {str(e)}")
                continue
    
    except Exception as e:
        print(f"Error al scrapear InfoJobs: {str(e)}")
    
    return ofertas

def scrape_linkedin(titulo: str = '', ubicacion: str = '') -> List[Dict[str, Any]]:
    """
    Scrape ofertas de trabajo de LinkedIn
    """
    ofertas = []
    base_url = 'https://www.linkedin.com'
    search_url = f'{base_url}/jobs/search'
    
    params = {}
    if titulo:
        params['keywords'] = titulo
    if ubicacion:
        params['location'] = ubicacion
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all('div', class_='job-card-container')
        
        for card in job_cards:
            try:
                title = card.find('h3', class_='base-search-card__title').text.strip()
                company = card.find('h4', class_='base-search-card__subtitle').text.strip()
                location = card.find('span', class_='job-search-card__location').text.strip()
                
                # Extraer salario si está disponible
                salary_text = card.find('span', class_='job-search-card__salary-info')
                min_salary = max_salary = 0
                if salary_text:
                    salary_match = re.search(r'(\d+)[kK]?\s*-\s*(\d+)[kK]?', salary_text.text)
                    if salary_match:
                        min_salary = int(salary_match.group(1)) * 1000
                        max_salary = int(salary_match.group(2)) * 1000
                
                # Extraer tipo de trabajo
                job_type = card.find('span', class_='job-search-card__job-type').text.strip()
                
                # Obtener descripción y requisitos
                job_url = base_url + card.find('a')['href']
                job_response = requests.get(job_url)
                job_soup = BeautifulSoup(job_response.text, 'html.parser')
                
                description = job_soup.find('div', class_='show-more-less-html__markup').text.strip()
                requirements = job_soup.find('div', class_='job-criteria-item__text').text.strip()
                
                # Extraer habilidades de la descripción y requisitos
                habilidades = extract_habilidades(description + ' ' + requirements)
                
                oferta = {
                    'title': title,
                    'company': company,
                    'location': location,
                    'min_salary': min_salary,
                    'max_salary': max_salary,
                    'job_type': job_type,
                    'description': description,
                    'requirements': requirements,
                    'publication_date': datetime.now().strftime('%Y-%m-%d'),
                    'fuente': 'LinkedIn',
                    'habilidades': habilidades
                }
                
                ofertas.append(oferta)
                
            except Exception as e:
                print(f"Error al procesar oferta de LinkedIn: {str(e)}")
                continue
    
    except Exception as e:
        print(f"Error al scrapear LinkedIn: {str(e)}")
    
    return ofertas

def extract_habilidades(texto: str) -> List[str]:
    """
    Extrae habilidades del texto de la descripción y requisitos
    """
    # Lista de habilidades comunes en tecnología
    habilidades_comunes = [
        'Python', 'Java', 'JavaScript', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust',
        'HTML', 'CSS', 'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask',
        'Spring', 'Laravel', 'Express', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis',
        'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Linux', 'Git', 'CI/CD',
        'DevOps', 'Agile', 'Scrum', 'JIRA', 'Jenkins', 'Terraform', 'Ansible',
        'Machine Learning', 'Data Science', 'Big Data', 'AI', 'IoT', 'Blockchain',
        'Microservices', 'REST API', 'GraphQL', 'WebSocket', 'gRPC', 'Kafka',
        'RabbitMQ', 'Elasticsearch', 'Kibana', 'Logstash', 'Prometheus', 'Grafana'
    ]
    
    # Convertir el texto a minúsculas para comparación
    texto = texto.lower()
    
    # Buscar habilidades en el texto
    habilidades_encontradas = []
    for habilidad in habilidades_comunes:
        if habilidad.lower() in texto:
            habilidades_encontradas.append(habilidad)
    
    return habilidades_encontradas 