# datos_externos/infojobs_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from django.utils import timezone
import time
from .utils import SALARIO_PATTERN, TIPO_TRABAJO_KEYWORDS

def scrape_infojobs(titulo='', ubicacion=''):
    url = "https://www.infojobs.net/ofertas-trabajo/"
    if titulo or ubicacion:
        url += "?"
        if titulo:
            url += f"keyword={titulo.replace(' ', '+')}"
        if ubicacion:
            url += f"&location={ubicacion.replace(' ', '+')}" if titulo else f"location={ubicacion.replace(' ', '+')}"
    
    options = Options()
    options.headless = False
    service = Service(executable_path="C:/Users/Bamba/Desktop/Proyectos/appwebmercado/chromedriver-win64/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        print("Por favor, completa la verificación manual en la ventana del navegador. Tienes 60 segundos...")
        time.sleep(60)
        
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sui-AtomCard")))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ofertas = []
        for oferta in soup.select('.sui-AtomCard'):
            titulo_elem = oferta.select_one('.ij-OfferCardContent-description-title-link')
            empresa_elem = oferta.select_one('.ij-OfferCardContent-description-subtitle-link')
            ubicacion_elem = oferta.select_one('.ij-OfferCardContent-description-list-item span')
            descripcion_elem = oferta.select_one('.ij-OfferCardContent-description-description')
            salario_elem = oferta.select_one('.ij-OfferCardContent-description-salary-info')

            titulo_oferta = titulo_elem.text.strip() if titulo_elem else "Sin título"
            empresa = empresa_elem.text.strip() if empresa_elem else "Sin empresa"
            ubicacion_oferta = ubicacion_elem.text.strip() if ubicacion_elem else ""
            habilidades = []
            descripcion = descripcion_elem.text.strip() if descripcion_elem else ""
            salario_raw = salario_elem.text.strip() if salario_elem else ""
            if not salario_raw and ("salario" in descripcion.lower() or "€" in descripcion or "k" in descripcion.lower()):
                salario_raw = descripcion

            # Buscar salario
            salario = ""
            if salario_raw:
                matches = SALARIO_PATTERN.findall(salario_raw)
                if matches and "Más de" not in salario_raw:
                    salario = next((m for m in matches if '-' in m), matches[0])

            # Extraer habilidades desde la descripción
            palabras_clave = ['Java', 'Spring', 'Node.js', 'Python', 'SQL', 'TypeScript', '.NET', 'C#', 'PHP', 'C++', 'R', 'Data', 'JavaScript', 'React', 'Angular']
            habilidades = [palabra for palabra in palabras_clave if palabra.lower() in descripcion.lower()]

            # Determinar tipo de trabajo
            tipo_trabajo = "No especificado"
            texto_lower = (ubicacion_oferta + " " + descripcion).lower()
            for tipo, keywords in TIPO_TRABAJO_KEYWORDS.items():
                if any(kw in texto_lower for kw in keywords):
                    tipo_trabajo = tipo
                    break

            print(f"Título encontrado: \"{titulo_oferta}\"")
            print(f"Empresa encontrada: \"{empresa}\"")
            print(f"Ubicación encontrada: \"{ubicacion_oferta}\"")
            print(f"Tipo de trabajo: \"{tipo_trabajo}\"")
            print(f"Salario encontrado: \"{salario}\"")
            print(f"Habilidades encontradas: {habilidades}")

            ofertas.append({
                'titulo': titulo_oferta,
                'empresa': empresa,
                'ubicacion': ubicacion_oferta,
                'habilidades': habilidades,
                'tipo_trabajo': tipo_trabajo,
                'salario': salario,
                'fecha_publicacion': timezone.now().date(),
                'fuente': 'InfoJobs'
            })
        return ofertas
    except Exception as e:
        print(f"Error en scrape_infojobs: {e}")
        return []
    finally:
        driver.quit()