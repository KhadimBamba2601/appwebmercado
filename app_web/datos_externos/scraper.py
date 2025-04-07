import os
import sys
import django
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from django.utils import timezone
from linkedin_api import Linkedin

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_web.settings')
django.setup()

from analisis_mercado.models import OfertaEmpleo, Habilidad

def scrape_tecnoempleo(titulo='', ubicacion=''):
    url = "https://www.tecnoempleo.com/ofertas-trabajo/"
    if titulo or ubicacion:
        url += "?"
        if titulo:
            url += f"keywords={titulo.replace(' ', '+')}"
        if ubicacion:
            url += f"&provincia={ubicacion.replace(' ', '+')}" if titulo else f"provincia={ubicacion.replace(' ', '+')}"
    
    options = Options()
    options.headless = True
    service = Service(executable_path="C:/Users/Bamba/Desktop/Proyectos/appwebmercado/chromedriver-win64/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "p-3")))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ofertas = []
        for oferta in soup.select('.p-3.border.rounded.mb-3.bg-white'):
            titulo_elem = oferta.select_one('h3.fs-5.mb-2 a')
            empresa_elem = oferta.select_one('.text-primary.link-muted')
            ubicacion_elem = oferta.select_one('.col-12.col-lg-3.text-gray-700 b')
            habilidades_elems = oferta.select('.hidden-md-down.text-gray-800 .badge')
            descripcion_elem = oferta.select_one('.text-gray-800')

            titulo_oferta = titulo_elem.text.strip() if titulo_elem else "Sin título"
            empresa = empresa_elem.text.strip() if empresa_elem else "Sin empresa"
            ubicacion_oferta = ubicacion_elem.text.strip() if ubicacion_elem else ""
            habilidades = [h.text.strip() for h in habilidades_elems] if habilidades_elems else []
            descripcion = descripcion_elem.text.strip() if descripcion_elem else ""

            # Determinar tipo de trabajo desde la descripción
            tipo_trabajo = "No especificado"
            if "presencial" in descripcion.lower():
                tipo_trabajo = "Presencial"
            elif "híbrido" in descripcion.lower() or "hibrido" in descripcion.lower():
                tipo_trabajo = "Híbrido"
            elif "remoto" in descripcion.lower():
                tipo_trabajo = "Remoto"

            print(f"Título encontrado: \"{titulo_oferta}\"")
            

            ofertas.append({
                'titulo': titulo_oferta,
                'empresa': empresa,
                'ubicacion': ubicacion_oferta,
                'habilidades': habilidades,
                'tipo_trabajo': tipo_trabajo,
                'fecha_publicacion': timezone.now().date(),
                'fuente': 'Tecnoempleo'
            })
        return ofertas
    finally:
        driver.quit()

def scrape_infojobs(titulo='', ubicacion=''):
    """Esqueleto para InfoJobs (sin configuración por ahora)."""
    print("InfoJobs no configurado: API no operativa temporalmente.")
    return []  # Devolver lista vacía hasta que configuremos la API

def scrape_linkedin(titulo='', ubicacion=''):
    """Scrape ofertas de LinkedIn usando la librería no oficial linkedin-api."""
    try:
        api = Linkedin("trabajoempresakn@gmail.com", "1stanc321")
        
        params = {}
        if titulo:
            params['keywords'] = titulo
        if ubicacion:
            params['location'] = ubicacion
        
        empleos = api.search_jobs(**params, limit=25)  # Reducido a 25 para evitar sobrecarga
        print(f"Encontradas {len(empleos)} ofertas en LinkedIn")
        
        ofertas = []
        for empleo in empleos:
            tracking_urn = empleo.get('trackingUrn', '')
            if tracking_urn:
                job_id = tracking_urn.split(':')[-1]
                job_details = api.get_job(job_id)
                
                titulo_oferta = job_details.get('title', 'Sin título')
                company_details = job_details.get('companyDetails', {}).get('com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany', {})
                empresa = company_details.get('companyResolutionResult', {}).get('name', 'Sin empresa')
                ubicacion_oferta = job_details.get('formattedLocation', '')
                
                # Determinar tipo de trabajo desde workplaceTypes
                workplace_types = job_details.get('workplaceTypes', [])
                workplace_resolutions = job_details.get('workplaceTypesResolutionResults', {})
                tipo_trabajo = "No especificado"
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
                
                # Extraer habilidades de la descripción
                habilidades = job_details.get('skills', [])
                if not habilidades:
                    descripcion = job_details.get('description', {}).get('text', '')
                    palabras_clave = ['Java', 'Spring', 'Node.js', 'Python', 'SQL', 'TypeScript', '.NET', 'C#', 'PHP', 'C++', 'R', 'Data', 'JavaScript', 'React', 'Angular']
                    habilidades = [palabra for palabra in palabras_clave if palabra.lower() in descripcion.lower()]

                print(f"Título encontrado: \"{titulo_oferta}\"")
                

                ofertas.append({
                    'titulo': titulo_oferta,
                    'empresa': empresa,
                    'ubicacion': ubicacion_oferta,
                    'habilidades': habilidades,
                    'tipo_trabajo': tipo_trabajo,
                    'fecha_publicacion': timezone.now().date(),
                    'fuente': 'LinkedIn'
                })
            else:
                print(f"No se encontró trackingUrn para el empleo: {empleo}")
        
        return ofertas
    except Exception as e:
        print(f"Error en scrape_linkedin: {e}")
        return []

def limpiar_ofertas_por_fuente(fuente):
    try:
        num_eliminadas, _ = OfertaEmpleo.objects.filter(fuente=fuente).delete()
        print(f"Eliminadas {num_eliminadas} ofertas antiguas de {fuente}.")
    except Exception as e:
        print(f"Error al eliminar ofertas de {fuente}: {e}")

def guardar_ofertas(ofertas):
    if ofertas:
        fuente = ofertas[0]['fuente']
        limpiar_ofertas_por_fuente(fuente)
    
    for oferta_data in ofertas:
        oferta, created = OfertaEmpleo.objects.get_or_create(
            titulo=oferta_data['titulo'],
            empresa=oferta_data['empresa'],
            defaults={
                'ubicacion': oferta_data['ubicacion'],
                'salario': oferta_data.get('salario', ''),
                'tipo_trabajo': oferta_data.get('tipo_trabajo', 'No especificado'),
                'fecha_publicacion': oferta_data['fecha_publicacion'],
                'fuente': oferta_data['fuente']
            }
        )
        for habilidad_nombre in oferta_data['habilidades']:
            habilidad_nombre = str(habilidad_nombre)[:200]
            habilidad, _ = Habilidad.objects.get_or_create(nombre=habilidad_nombre)
            oferta.habilidades.add(habilidad)

if __name__ == "__main__":
    try:
        # Probar Tecnoempleo
        ofertas_tecno = scrape_tecnoempleo(titulo="programador", ubicacion="Madrid")
        guardar_ofertas(ofertas_tecno)
        print(f"Guardadas {len(ofertas_tecno)} ofertas de Tecnoempleo.")
        
        # Probar LinkedIn
        ofertas_linkedin = scrape_linkedin(titulo="programador", ubicacion="Madrid")
        guardar_ofertas(ofertas_linkedin)
        print(f"Guardadas {len(ofertas_linkedin)} ofertas de LinkedIn.")
        
        # Probar InfoJobs (sin configuración)
        ofertas_infojobs = scrape_infojobs(titulo="programador", ubicacion="Madrid")
        guardar_ofertas(ofertas_infojobs)
        print(f"Guardadas {len(ofertas_infojobs)} ofertas de InfoJobs.")
    except Exception as e:
        print(f"Error durante la ejecución: {e}")