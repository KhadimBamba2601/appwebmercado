import requests
from datetime import datetime
from bs4 import BeautifulSoup
from .base import BaseScraper
from ...usuarios.models import Habilidad
import re

class InfoJobsScraper(BaseScraper):
    def __init__(self, fuente_datos):
        super().__init__(fuente_datos)
        self.api_key = fuente_datos.api_key
        self.headers = {
            'Authorization': f'Basic {self.api_key}',
            'Content-Type': 'application/json'
        }
        self.base_url = 'https://api.infojobs.net/api/9/offer'

    def obtener_ofertas(self, max_paginas=1):
        """
        Obtiene ofertas de empleo de InfoJobs usando su API.
        """
        ofertas = []
        pagina = 1
        
        while pagina <= max_paginas:
            try:
                params = {
                    'page': pagina,
                    'maxResults': 50,
                    'orderBy': 'relevance',
                    'sortOrder': 'desc'
                }
                
                response = requests.get(
                    self.base_url,
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code != 200:
                    self.logger.error(f"Error en la API de InfoJobs: {response.status_code}")
                    break
                
                data = response.json()
                if not data.get('items'):
                    break
                
                for item in data['items']:
                    oferta = self._procesar_oferta(item)
                    if oferta:
                        ofertas.append(oferta)
                
                pagina += 1
                
            except Exception as e:
                self.logger.error(f"Error al obtener ofertas de InfoJobs: {str(e)}")
                break
        
        return ofertas

    def _procesar_oferta(self, item):
        """
        Procesa los datos de una oferta de InfoJobs.
        """
        try:
            # Extraer habilidades del título y descripción
            habilidades = self._extraer_habilidades(
                f"{item['title']} {item['description']}"
            )
            
            # Procesar salario
            salario = self._procesar_salario(item.get('salary', {}))
            
            datos_oferta = {
                'titulo': item['title'],
                'empresa': item['company']['name'],
                'descripcion': item['description'],
                'ubicacion': item['city'],
                'salario_min': salario.get('min'),
                'salario_max': salario.get('max'),
                'tipo_contrato': self._mapear_tipo_contrato(item.get('contractType')),
                'fecha_publicacion': datetime.fromisoformat(item['published']),
                'url_original': item['link'],
                'habilidades': habilidades
            }
            
            return self.guardar_oferta(datos_oferta)
            
        except Exception as e:
            self.logger.error(f"Error al procesar oferta: {str(e)}")
            return None

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

    def _procesar_salario(self, salario_data):
        """
        Procesa la información de salario de InfoJobs.
        """
        if not salario_data:
            return {}
            
        try:
            min_salary = salario_data.get('min', {}).get('value')
            max_salary = salario_data.get('max', {}).get('value')
            
            return {
                'min': float(min_salary) if min_salary else None,
                'max': float(max_salary) if max_salary else None
            }
        except (ValueError, TypeError):
            return {}

    def _mapear_tipo_contrato(self, tipo_infojobs):
        """
        Mapea el tipo de contrato de InfoJobs al formato interno.
        """
        mapeo = {
            'FULL_TIME': 'INDEF',
            'PART_TIME': 'TEMP',
            'INTERNSHIP': 'PRAC',
            'TEMPORARY': 'TEMP',
            'CONTRACT': 'TEMP',
            'OTHER': 'OTRO'
        }
        return mapeo.get(tipo_infojobs, 'OTRO') 