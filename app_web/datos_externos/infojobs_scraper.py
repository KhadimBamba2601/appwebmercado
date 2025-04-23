# datos_externos/infojobs_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from django.utils import timezone
import time
import random
from .utils import SALARIO_PATTERN, TIPO_TRABAJO_KEYWORDS

def scrape_infojobs(titulo='', ubicacion=''):
    url = "https://www.infojobs.net/ofertas-trabajo/"
    if titulo or ubicacion:
        url += "?"
        if titulo:
            url += f"keyword={titulo.replace(' ', '+')}"
        if ubicacion:
            url += f"&location={ubicacion.replace(' ', '+')}" if titulo else f"location={ubicacion.replace(' ', '+')}"
    
    # Configuración de Selenium para simular un navegador humano
    options = Options()
    options.headless = False  # Necesario para verificación manual
    options.add_argument("--disable-blink-features=AutomationControlled")  # Evitar detección de bot
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    service = Service(executable_path="C:/Users/Bamba/Desktop/Proyectos/appwebmercado/chromedriver-win64/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        time.sleep(15)  # Tiempo para CAPTCHA o verificación
        
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 1
        max_attempts = 3 
        while scroll_attempts < max_attempts:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 4))  # Espera aleatoria para simular humano
            # Simular movimiento del ratón
            ActionChains(driver).move_by_offset(random.randint(10, 50), random.randint(10, 50)).perform()
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                scroll_attempts += 1
                print(f"Intento {scroll_attempts}/{max_attempts}: Sin cambios en altura.")
            else:
                scroll_attempts = 0
            last_height = new_height
        
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sui-AtomCard")))
        
        # Extraer todas las ofertas directamente con Selenium
        oferta_elements = driver.find_elements(By.CLASS_NAME, "sui-AtomCard")
        
        ofertas = []
        for i, oferta in enumerate(oferta_elements, 1):
            try:
                # Extraer datos con Selenium
                titulo_elem = oferta.find_element(By.CLASS_NAME, 'ij-OfferCardContent-description-title-link')
                empresa_elem = oferta.find_elements(By.CLASS_NAME, 'ij-OfferCardContent-description-subtitle-link')
                ubicacion_elem = oferta.find_elements(By.CSS_SELECTOR, '.ij-OfferCardContent-description-list-item span')
                descripcion_elem = oferta.find_elements(By.CLASS_NAME, 'ij-OfferCardContent-description-description')
                salario_elem = oferta.find_elements(By.CLASS_NAME, 'ij-OfferCardContent-description-salary-info')

                # Procesar datos
                titulo_oferta = titulo_elem.text.strip() if titulo_elem else "Sin título"
                url_oferta = titulo_elem.get_attribute('href') if titulo_elem else ""
                if not url_oferta.startswith('http'):
                    url_oferta = "https://www.infojobs.net" + url_oferta
                
                empresa = empresa_elem[0].text.strip() if empresa_elem else "Sin empresa"
                ubicacion_oferta = ubicacion_elem[0].text.strip() if ubicacion_elem else ""
                descripcion = descripcion_elem[0].text.strip() if descripcion_elem else ""
                salario_raw = salario_elem[0].text.strip() if salario_elem else ""
                if not salario_raw and ("salario" in descripcion.lower() or "€" in descripcion or "k" in descripcion.lower()):
                    salario_raw = descripcion

                # Buscar salario
                salario = ""
                if salario_raw:
                    matches = SALARIO_PATTERN.findall(salario_raw)
                    if matches and "Más de" not in salario_raw:
                        salario = next((m for m in matches if '-' in m), matches[0])

                # Extraer habilidades
                palabras_clave = ['Java', 'Spring', 'Node.js', 'Python', 'API', 'SQL', 'TypeScript', '.NET', 'C#', 'PHP', 'C++', 'Azure', 'Android', 'Apple', 'Front-end', 'Frontend', 'Backend', 'Git', 'PMP', 'informatica', 'ciberseguridad', 'Zapier', 'ChatGPT', 'Chat GPT', 'Back-end', 'Swift', 'HTML5', 'Data', 'windows', 'Jira', 'Selenium', 'cobol', 'Linux', 'Software', 'JavaScript', 'React', 'Angular']
                habilidades = [palabra for palabra in palabras_clave if palabra.lower() in descripcion.lower()]

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
                    'fecha_publicacion': timezone.now().date(),
                    'fuente': 'InfoJobs',
                    'url': url_oferta
                })
            except Exception as e:
                print(f"Error procesando oferta {i}: {e}")
                continue
        
        print(f"Total de ofertas procesadas: {len(ofertas)}")
        return ofertas
    except Exception as e:
        print(f"Error en scrape_infojobs: {e}")
        return []
    finally:
        driver.quit()
