# datos_externos/tecnoempleo_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import date
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
            salario_elem = oferta.select_one('.col-12.col-lg-3.text-gray-700.pt-2.text-right.hidden-md-down')

            titulo_oferta = titulo_elem.text.strip() if titulo_elem else "Sin título"
            empresa = empresa_elem.text.strip() if empresa_elem else "Sin empresa"
            ubicacion_oferta = ubicacion_elem.text.strip() if ubicacion_elem else ""
            habilidades = [h.text.strip() for h in habilidades_elems] if habilidades_elems else []
            descripcion = descripcion_elem.text.strip() if descripcion_elem else ""
            salario_raw = salario_elem.text.strip() if salario_elem else ""
            
            print(f"Salario crudo (Tecnoempleo): \"{salario_raw}\"")
            
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
                'fecha_publicacion': date.today(),
                'fuente': 'Tecnoempleo'
            })
        return ofertas
    finally:
        driver.quit()