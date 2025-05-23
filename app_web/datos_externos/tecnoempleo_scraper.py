# datos_externos/tecnoempleo_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import date
import os
from .utils import SALARIO_PATTERN, TIPO_TRABAJO_KEYWORDS

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
    
    # Obtener la ruta absoluta del directorio del proyecto
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    chromedriver_path = os.path.join(base_dir, 'chromedriver-win64', 'chromedriver-win64', 'chromedriver.exe')
    
    service = Service(executable_path=chromedriver_path)
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
            salario_elem = oferta.select_one('.col-12.col-lg-3.text-gray-700.pt-2.text-right.hidden-md-down')

            # Extraer título y URL
            titulo_oferta = titulo_elem.text.strip() if titulo_elem else "Sin título"
            href = titulo_elem['href'] if titulo_elem and 'href' in titulo_elem.attrs else ""
            # Comprobar si el href es relativo o absoluto
            if href.startswith('http'):
                url_oferta = href  # Ya es una URL absoluta
            else:
                url_oferta = "https://www.tecnoempleo.com" + href  # Añadir prefijo si es relativo
            
            empresa = empresa_elem.text.strip() if empresa_elem else "Sin empresa"
            ubicacion_oferta = ubicacion_elem.text.strip() if ubicacion_elem else ""
            habilidades = [h.text.strip() for h in habilidades_elems] if habilidades_elems else []
            descripcion = descripcion_elem.text.strip() if descripcion_elem else ""
            salario_raw = salario_elem.text.strip() if salario_elem else ""

            # Buscar salario
            salario = ""
            texto_completo = salario_raw + " " + descripcion
            matches = SALARIO_PATTERN.findall(texto_completo)
            if matches:
                salario = next((m for m in matches if '-' in m), matches[0])

            # Determinar tipo de trabajo
            tipo_trabajo = "No especificado"
            texto_lower = (ubicacion_oferta + " " + descripcion).lower()
            for tipo, keywords in TIPO_TRABAJO_KEYWORDS.items():
                if any(kw in texto_lower for kw in keywords):
                    tipo_trabajo = tipo
                    break

            ofertas.append({
                'titulo': titulo_oferta,
                'empresa': empresa,
                'ubicacion': ubicacion_oferta,
                'habilidades': habilidades,
                'tipo_trabajo': tipo_trabajo,
                'salario': salario,
                'fecha_publicacion': date.today(),
                'fuente': 'Tecnoempleo',
                'url': url_oferta
            })
        print(f"Total de ofertas procesadas: {len(ofertas)}")
        return ofertas
    except Exception as e:
        print(f"Error en scrape_tecnoempleo: {e}")
        return []
    finally:
        driver.quit()