from abc import ABC, abstractmethod
from django.conf import settings
from ..models import FuenteDatos, OfertaEmpleo
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self, fuente_datos):
        self.fuente = fuente_datos
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    def obtener_ofertas(self, max_paginas=1):
        """
        Obtiene ofertas de empleo de la fuente.
        Args:
            max_paginas: Número máximo de páginas a scrapear
        Returns:
            list: Lista de ofertas encontradas
        """
        pass

    def guardar_oferta(self, datos_oferta):
        """
        Guarda una oferta en la base de datos.
        Args:
            datos_oferta: Diccionario con los datos de la oferta
        Returns:
            OfertaEmpleo: Instancia de la oferta guardada
        """
        try:
            oferta = OfertaEmpleo.objects.create(
                titulo=datos_oferta['titulo'],
                empresa=datos_oferta['empresa'],
                descripcion=datos_oferta['descripcion'],
                ubicacion=datos_oferta['ubicacion'],
                salario_min=datos_oferta.get('salario_min'),
                salario_max=datos_oferta.get('salario_max'),
                tipo_contrato=datos_oferta.get('tipo_contrato', 'OTRO'),
                fecha_publicacion=datos_oferta['fecha_publicacion'],
                url_original=datos_oferta['url_original'],
                fuente=self.fuente
            )
            
            if 'habilidades' in datos_oferta:
                oferta.habilidades_requeridas.set(datos_oferta['habilidades'])
            
            self.logger.info(f"Oferta guardada: {oferta.titulo}")
            return oferta
            
        except Exception as e:
            self.logger.error(f"Error al guardar oferta: {str(e)}")
            return None

    def actualizar_fuente(self):
        """
        Actualiza la fecha de última actualización de la fuente.
        """
        self.fuente.ultima_actualizacion = datetime.now()
        self.fuente.save() 