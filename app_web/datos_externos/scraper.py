import os
import sys
import django
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from django.utils import timezone

# Agregar el directorio del proyecto al path de Python
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_web.settings')
django.setup()

# Importar modelos después de configurar Django
from analisis_mercado.models import OfertaEmpleo, Habilidad

def scrape_tecnoempleo():
    url = "https://www.tecnoempleo.com/ofertas-trabajo/"
    
    # Configurar Selenium
    options = Options()
    options.headless = True  # Ejecutar sin abrir la ventana del navegador
    service = Service(executable_path="C:/Users/Bamba/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")  # Ajusta esta ruta
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        # Opcional: espera explícita si el contenido tarda en cargar (descomenta si es necesario)
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "p-3")))
        
        # Obtener el HTML completo después de que la página se haya cargado
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        print("HTML recibido:")
        print(f"Encontradas {len(soup.select('.p-3.border.rounded.mb-3.bg-white'))} ofertas")
        
        ofertas = []
        for oferta in soup.select('.p-3.border.rounded.mb-3.bg-white'):  # Selector ajustado previamente
            # Ajusta los selectores según inspección
            titulo_elem = oferta.find(class_='fs-5.mb-2')
            empresa_elem = oferta.find(class_='text-primary.link-muted')
            ubicacion_elem = oferta.find(class_='d-block.d-lg-none.text-gray-800')
            habilidades_elems = oferta.select('.col-12.col-lg-3.text-gray-700.pt-2.text-right.hidden-md-down')

            titulo = titulo_elem.text.strip() if titulo_elem else "Sin título"
            empresa = empresa_elem.text.strip() if empresa_elem else "Sin empresa"
            ubicacion = ubicacion_elem.text.strip() if ubicacion_elem else ""
            habilidades = [h.text.strip() for h in habilidades_elems] if habilidades_elems else []

            ofertas.append({
                'titulo': titulo,
                'empresa': empresa,
                'ubicacion': ubicacion,
                'habilidades': habilidades,
                'fecha_publicacion': timezone.now().date(),
                'fuente': 'Tecnoempleo'
            })
        return ofertas
    
    finally:
        driver.quit()  # Asegura que el navegador se cierre siempre

def guardar_ofertas(ofertas):
    for oferta_data in ofertas:
        oferta, created = OfertaEmpleo.objects.get_or_create(
            titulo=oferta_data['titulo'],
            empresa=oferta_data['empresa'],
            defaults={
                'ubicacion': oferta_data['ubicacion'],
                'salario': oferta_data.get('salario', ''),
                'fecha_publicacion': oferta_data['fecha_publicacion'],
                'fuente': oferta_data['fuente']
            }
        )
        for habilidad_nombre in oferta_data['habilidades']:
            habilidad, _ = Habilidad.objects.get_or_create(nombre=habilidad_nombre)
            oferta.habilidades.add(habilidad)

if __name__ == "__main__":
    try:
        ofertas = scrape_tecnoempleo()
        guardar_ofertas(ofertas)
        print(f"Guardadas {len(ofertas)} ofertas de Tecnoempleo.")
    except Exception as e:
        print(f"Error durante la ejecución: {e}")