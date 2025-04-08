# datos_externos/scraper.py
from .tecnoempleo_scraper import scrape_tecnoempleo
from .linkedin_scraper import scrape_linkedin
from .infojobs_scraper import scrape_infojobs
from .utils import guardar_ofertas

def main():
    try:
        # Scraping de Tecnoempleo
        ofertas_tecno = scrape_tecnoempleo(titulo="programador", ubicacion="Madrid")
        guardar_ofertas(ofertas_tecno)
        print(f"Guardadas {len(ofertas_tecno)} ofertas de Tecnoempleo.")
        
        # Scraping de LinkedIn
        ofertas_linkedin = scrape_linkedin(titulo="programador", ubicacion="Madrid")
        guardar_ofertas(ofertas_linkedin)
        print(f"Guardadas {len(ofertas_linkedin)} ofertas de LinkedIn.")
        
        # Scraping de InfoJobs
        ofertas_infojobs = scrape_infojobs(titulo="programador", ubicacion="Madrid")
        guardar_ofertas(ofertas_infojobs)
        print(f"Guardadas {len(ofertas_infojobs)} ofertas de InfoJobs.")
    except Exception as e:
        print(f"Error durante la ejecución: {e}")

if __name__ == "__main__":
    main()