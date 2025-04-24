# test_linkedin_scraper.py
import os
import sys
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("test_linkedin_scraper.log"),  # Guardar logs en un archivo
        logging.StreamHandler()  # Mostrar logs en consola
    ]
)

# Añadir el directorio raíz al path para que Python pueda encontrar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_web.datos_externos.linkedin_scraper import scrape_linkedin

def test_scraper():
    logging.info("Iniciando búsqueda de ofertas de trabajo")
    try:
        # Prueba con búsqueda de desarrollador en España
        resultados = scrape_linkedin(titulo="desarrollador", ubicacion="Madrid")
        
        # Imprimir resultados de forma legible
        logging.info(f"Resultados encontrados: {len(resultados)}")
        print(f"\nResultados encontrados: {len(resultados)}")
        for i, oferta in enumerate(resultados, 1):
            print("\n" + "="*50)
            print(f"Oferta {i}:")
            print(f"Título: {oferta['titulo']}")
            print(f"Empresa: {oferta['empresa']}")
            print(f"Ubicación: {oferta['ubicacion']}")
            print(f"Tipo de trabajo: {oferta['tipo_trabajo']}")
            print(f"Salario: {oferta['salario']}")
            print(f"URL: {oferta['url']}")
            if oferta['habilidades']:
                print(f"Habilidades: {', '.join(oferta['habilidades'])}")
            print(f"Fecha publicación: {oferta['fecha_publicacion']}")
            print(f"Fuente: {oferta['fuente']}")
            logging.debug(f"Detalles de oferta {i}: {oferta}")
    
    except Exception as e:
        logging.error(f"Error en test_scraper: {str(e)}", exc_info=True)
        print(f"Error en test_scraper: {str(e)}")

if __name__ == "__main__":
    test_scraper()