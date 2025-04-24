import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        # Datos de ejemplo para desarrollo
        self.ofertas = []
        self.habilidades = []
        self.usuarios = []

    def connect(self):
        # Simulación de conexión exitosa
        return True

    def disconnect(self):
        pass

    def execute_query(self, query, params=None):
        # Simulación de ejecución exitosa
        return True

    def fetch_all(self, query, params=None):
        # Retornar datos de ejemplo según la consulta
        if "ofertas_empleo" in query:
            return self.ofertas
        elif "habilidades" in query:
            return self.habilidades
        elif "usuarios" in query:
            return self.usuarios
        return []

    def fetch_one(self, query, params=None):
        # Retornar un registro de ejemplo
        if "ofertas_empleo" in query:
            return (1, "Desarrollador Python", "Empresa Ejemplo", "Madrid", "Tiempo completo", "30000-40000", "http://ejemplo.com", ["Python", "Django"])
        elif "habilidades" in query:
            return (1, "Python", "Lenguaje de programación")
        elif "usuarios" in query:
            return (1, "admin", "admin@ejemplo.com", "Administrador")
        return None 