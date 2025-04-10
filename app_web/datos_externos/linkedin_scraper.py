# datos_externos/linkedin_scraper.py
from linkedin_api import Linkedin
from django.utils import timezone
from .utils import SALARIO_PATTERN, TIPO_TRABAJO_KEYWORDS

def scrape_linkedin(titulo='', ubicacion=''):
    try:
        api = Linkedin("trabajoempresakn@gmail.com", "1stanc321")  # Reemplaza con tus credenciales
        
        params = {}
        if titulo:
            params['keywords'] = titulo
        if ubicacion:
            params['location'] = ubicacion
        
        empleos = api.search_jobs(**params, limit=25)
        print(f"Encontradas {len(empleos)} ofertas en LinkedIn")
        
        ofertas = []
        for empleo in empleos:
            tracking_urn = empleo.get('trackingUrn', '')
            if tracking_urn:
                job_id = tracking_urn.split(':')[-1]
                job_details = api.get_job(job_id)
                
                # Construir la URL de la oferta
                url_oferta = f"https://www.linkedin.com/jobs/view/{job_id}"
                
                titulo_oferta = job_details.get('title', 'Sin título')
                company_details = job_details.get('companyDetails', {}).get('com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany', {})
                empresa = company_details.get('companyResolutionResult', {}).get('name', 'Sin empresa')
                ubicacion_oferta = job_details.get('formattedLocation', '')
                
                # Determinar tipo de trabajo
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
                
                # Extraer habilidades y salario
                habilidades = job_details.get('skills', [])
                if not habilidades:
                    palabras_clave = ['Java', 'Spring', 'Node.js', 'Python','API', 'SQL', 'TypeScript', '.NET', 'C#', 'PHP', 'C++', 'Azure', 'Android', 'iOS', 'Front-end','Forntend', 'Backend','Git','PMP','informatica', 'ciberseguridad','Zapier', 'ChatGPT','Chat GPT', 'Back-end', 'Swift', 'HTML5', 'Data', 'windows','Jira','Selenium', 'cobol','Linux','Software', 'JavaScript', 'React', 'Angular']
                    habilidades = [palabra for palabra in palabras_clave if palabra.lower() in descripcion.lower()]
                
                salario_raw = descripcion if ("salario" in descripcion.lower() or "salary" in descripcion.lower() or "€" in descripcion or "k" in descripcion.lower()) else ""
                salario_raw += " " + titulo_oferta
                
                salario = ""
                if salario_raw:
                    matches = SALARIO_PATTERN.findall(salario_raw)
                    if matches:
                        salario = next((m for m in matches if '-' in m), matches[-1])

                ofertas.append({
                    'titulo': titulo_oferta,
                    'empresa': empresa,
                    'ubicacion': ubicacion_oferta,
                    'habilidades': habilidades,
                    'tipo_trabajo': tipo_trabajo,
                    'salario': salario,
                    'fecha_publicacion': timezone.now().date(),
                    'fuente': 'LinkedIn',
                    'url': url_oferta  # Añadimos la URL al diccionario
                })
            else:
                print(f"No se encontró trackingUrn para el empleo: {empleo}")
        
        return ofertas
    except Exception as e:
        print(f"Error en scrape_linkedin: {e}")
        return []