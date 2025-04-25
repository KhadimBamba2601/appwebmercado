import requests
from datetime import datetime
from bs4 import BeautifulSoup
from .base import BaseScraper
from ...usuarios.models import Habilidad
import re

class TecnoempleoScraper(BaseScraper):
    def __init__(self, fuente_datos):
        super().__init__(fuente_datos)
        self.base_url = 'https://www.tecnoempleo.com'
        self.search_url = f"{self.base_url}/buscar-ofertas-trabajo"

    def obtener_ofertas(self, max_paginas=1):
        """
        Obtiene ofertas de empleo de Tecnoempleo usando web scraping.
        """
        ofertas = []
        pagina = 1
        
        while pagina <= max_paginas:
            try:
                params = {
                    'pagina': pagina,
                    'orden': 'fecha',
                    'direccion': 'desc'
                }
                
                response = requests.get(
                    self.search_url,
                    params=params,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                
                if response.status_code != 200:
                    self.logger.error(f"Error al acceder a Tecnoempleo: {response.status_code}")
                    break
                
                soup = BeautifulSoup(response.text, 'html.parser')
                ofertas_pagina = soup.find_all('div', class_='oferta')
                
                if not ofertas_pagina:
                    break
                
                for oferta_html in ofertas_pagina:
                    oferta = self._procesar_oferta_html(oferta_html)
                    if oferta:
                        ofertas.append(oferta)
                
                pagina += 1
                
            except Exception as e:
                self.logger.error(f"Error al obtener ofertas de Tecnoempleo: {str(e)}")
                break
        
        return ofertas

    def _procesar_oferta_html(self, oferta_html):
        """
        Procesa el HTML de una oferta de Tecnoempleo.
        """
        try:
            titulo = oferta_html.find('h2', class_='titulo').text.strip()
            empresa = oferta_html.find('div', class_='empresa').text.strip()
            descripcion = oferta_html.find('div', class_='descripcion').text.strip()
            ubicacion = oferta_html.find('div', class_='ubicacion').text.strip()
            
            # Extraer URL
            url_element = oferta_html.find('a', class_='titulo')
            url_original = self.base_url + url_element['href'] if url_element else None
            
            # Extraer fecha
            fecha_texto = oferta_html.find('div', class_='fecha').text.strip()
            fecha_publicacion = self._parsear_fecha(fecha_texto)
            
            # Extraer salario
            salario_element = oferta_html.find('div', class_='salario')
            salario = self._procesar_salario(salario_element.text if salario_element else '')
            
            # Extraer habilidades
            habilidades = self._extraer_habilidades(f"{titulo} {descripcion}")
            
            datos_oferta = {
                'titulo': titulo,
                'empresa': empresa,
                'descripcion': descripcion,
                'ubicacion': ubicacion,
                'salario_min': salario.get('min'),
                'salario_max': salario.get('max'),
                'fecha_publicacion': fecha_publicacion,
                'url_original': url_original,
                'habilidades': habilidades
            }
            
            return self.guardar_oferta(datos_oferta)
            
        except Exception as e:
            self.logger.error(f"Error al procesar oferta HTML: {str(e)}")
            return None

    def _parsear_fecha(self, fecha_texto):
        """
        Convierte el texto de fecha de Tecnoempleo a datetime.
        """
        try:
            # Formato común: "Publicada el DD/MM/YYYY"
            fecha = re.search(r'(\d{2}/\d{2}/\d{4})', fecha_texto)
            if fecha:
                return datetime.strptime(fecha.group(1), '%d/%m/%Y')
            return datetime.now()
        except:
            return datetime.now()

    def _procesar_salario(self, texto_salario):
        """
        Procesa el texto de salario de Tecnoempleo.
        """
        try:
            # Patrón común: "XX.XXX€ - YY.YYY€"
            match = re.search(r'(\d{1,3}(?:\.\d{3})*)€\s*-\s*(\d{1,3}(?:\.\d{3})*)€', texto_salario)
            if match:
                min_salary = float(match.group(1).replace('.', ''))
                max_salary = float(match.group(2).replace('.', ''))
                return {'min': min_salary, 'max': max_salary}
            return {}
        except:
            return {}

    def _extraer_habilidades(self, texto):
        """
        Extrae habilidades del texto usando expresiones regulares y matching con habilidades existentes.
        """
        habilidades = set()
        # Lista de palabras clave comunes en tecnologías
        keywords = [
            'python', 'java', 'javascript', 'django', 'react', 'angular',
            'vue', 'node', 'sql', 'postgresql', 'mysql', 'mongodb',
            'docker', 'kubernetes', 'aws', 'azure', 'git', 'linux'
        ]
        
        texto = texto.lower()
        for keyword in keywords:
            if keyword in texto:
                habilidad, _ = Habilidad.objects.get_or_create(
                    nombre=keyword.capitalize(),
                    defaults={'categoria': 'Tecnología'}
                )
                habilidades.add(habilidad)
        
        return list(habilidades) 