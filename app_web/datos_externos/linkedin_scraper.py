# datos_externos/linkedin_scraper.py
from linkedin_api import Linkedin
from django.utils import timezone
from .utils import SALARIO_PATTERN, TIPO_TRABAJO_KEYWORDS
import logging
import time
import random

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("linkedin_scraper.log"),
        logging.StreamHandler()
    ]
)

def scrape_linkedin(titulo='', ubicacion=''):
    logging.info(f"Iniciando scrape_linkedin con título: '{titulo}', ubicación: '{ubicacion}'")
    try:
        logging.info("Intentando autenticación con LinkedIn API")
        api = Linkedin("trabajoempresakn@gmail.com", "1stanc321")
        logging.info("Autenticación exitosa")
        
        params = {}
        if titulo:
            params['keywords'] = 'developer'  # Cambiar a inglés
        if ubicacion:
            params['location'] = 'Spain'     # Ampliar la ubicación
        logging.info(f"Parámetros de búsqueda: {params}")
        
        logging.info("Realizando búsqueda de empleos")
        empleos = api.search_jobs(**params, limit=5)
        logging.info(f"Respuesta cruda de api.search_jobs: {empleos}")
        logging.info(f"Encontradas {len(empleos)} ofertas en LinkedIn")
        
        ofertas = []
        for empleo in empleos:
            time.sleep(random.uniform(2, 5))
            tracking_urn = empleo.get('trackingUrn', '')
            if tracking_urn:
                job_id = tracking_urn.split(':')[-1]
                logging.info(f"Obteniendo detalles del empleo ID: {job_id}")
                try:
                    job_details = api.get_job(job_id)
                    logging.info(f"Detalles obtenidos para empleo ID: {job_id}")
                    
                    url_oferta = f"https://www.linkedin.com/jobs/view/{job_id}"
                    titulo_oferta = job_details.get('title', 'Sin título')
                    company_details = job_details.get('companyDetails', {}).get('com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany', {})
                    empresa = company_details.get('companyResolutionResult', {}).get('name', 'Sin empresa')
                    ubicacion_oferta = job_details.get('formattedLocation', '')
                    
                    workplace_types = job_details.get('workplaceTypes', [])
                    workplace_resolutions = job_details.get('workplaceTypesResolutionResults', {})
                    tipo_trabajo = "No especificado"
                    descripcion = job_details.get('description', {}).get('text', '')
                    texto_lower = (ubicacion_oferta + " " + descripcion).lower()
                    for wpt in workplace_types:
                        if wpt in workplace_resolutions:
                            tipo = workplace_resolutions[wpt].get('localizedName', '')
                            if tipo == "On-site":
                                tipo_trabajo = "Presencial"
                            elif tipo == "Remote":
                                tipo_trabajo = "Remoto"
                            elif tipo == "Hybrid":
                                tipo_trabajo = "Híbrido"
                            break
                    if tipo_trabajo == "No especificado":
                        for tipo, keywords in TIPO_TRABAJO_KEYWORDS.items():
                            if any(kw in texto_lower for kw in keywords):
                                tipo_trabajo = tipo
                                break
                    
                    habilidades = job_details.get('skills', [])
                    if not habilidades:
                        palabras_clave = ['Java', 'Spring', 'Node.js', 'Python', 'API', 'REST', 'SQL', 'TypeScript', '.NET', 'C#', 'PHP', 'C++', 'Azure', 'Android', 'iOS', 'Front-end', 'Backend', 'Git', 'PMP', 'informatica', 'ciberseguridad', 'Zapier', 'ChatGPT', 'Back-end', 'Swift', 'HTML5', 'Data', 'UX', 'UI', 'windows', 'Jira', 'Selenium', 'cobol', 'Linux', 'Software', 'JavaScript', 'React', 'Angular']
                        habilidades = [palabra for palabra in palabras_clave if palabra.lower() in descripcion.lower()]
                    
                    salario_raw = descripcion if ("salario" in descripcion.lower() or "salary" in descripcion.lower() or "€" in descripcion or "k" in descripcion.lower()) else ""
                    salario_raw += " " + titulo_oferta
                    
                    salario = ""
                    if salario_raw:
                        matches = SALARIO_PATTERN.findall(salario_raw)
                        if matches:
                            salario = next((m for m in matches if '-' in m), matches[-1])
                    
                    logging.info(f"Procesado empleo: Título='{titulo_oferta}', Empresa='{empresa}', URL={url_oferta}")
                    logging.info(f"Tipo de trabajo: {tipo_trabajo}, Salario: {salario}, Habilidades: {habilidades}")
                    
                    ofertas.append({
                        'titulo': titulo_oferta,
                        'empresa': empresa,
                        'ubicacion': ubicacion_oferta,
                        'habilidades': habilidades,
                        'tipo_trabajo': tipo_trabajo,
                        'salario': salario,
                        'fecha_publicacion': timezone.now().date(),
                        'fuente': 'LinkedIn',
                        'url': url_oferta
                    })
                except Exception as e:
                    logging.error(f"Error al obtener detalles del empleo ID {job_id}: {str(e)}")
            else:
                logging.warning(f"No se encontró trackingUrn para el empleo: {empleo}")
        
        logging.info(f"Scraping completado. Total de ofertas procesadas: {len(ofertas)}")
        return ofertas
    
    except Exception as e:
        logging.error(f"Error en scrape_linkedin: {str(e)}", exc_info=True)
        return []