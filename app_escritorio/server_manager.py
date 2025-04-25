import os
import sys
import subprocess
import threading
import time
import signal
import logging
import requests
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app_escritorio.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ServerManager")

class DjangoServerManager(QObject):
    server_started = pyqtSignal()
    server_stopped = pyqtSignal()
    server_error = pyqtSignal(str)
    
    def __init__(self, port=8000):
        super().__init__()
        self.port = port
        self.process = None
        self.thread = None
        self.is_running = False
        self.server_url = f"http://localhost:{port}"
        
        # Obtener la ruta absoluta al directorio de la aplicación web
        self.base_dir = Path(__file__).resolve().parent.parent
        self.web_app_dir = self.base_dir / "app_web"
        
        # Verificar que el directorio de la aplicación web existe
        if not self.web_app_dir.exists():
            raise FileNotFoundError(f"No se encontró el directorio de la aplicación web en {self.web_app_dir}")
    
    def get_server_url(self):
        """Retorna la URL del servidor Django."""
        return self.server_url
    
    def start_server(self):
        """Inicia el servidor Django en un proceso separado."""
        if self.process is not None:
            logger.warning("El servidor ya está en ejecución")
            return True
        
        try:
            # Obtener la ruta del proyecto Django
            django_project_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app_web")
            
            # Comando para iniciar el servidor
            command = [
                sys.executable,
                "manage.py",
                "runserver",
                f"127.0.0.1:{self.port}"
            ]
            
            # Iniciar el proceso
            self.process = subprocess.Popen(
                command,
                cwd=django_project_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Esperar a que el servidor esté disponible
            max_attempts = 10
            attempt = 0
            while attempt < max_attempts:
                try:
                    response = requests.get(f"{self.server_url}/api/health/")
                    if response.status_code == 200:
                        logger.info("Servidor Django iniciado correctamente")
                        self.server_started.emit()
                        return True
                except requests.exceptions.ConnectionError:
                    time.sleep(1)
                    attempt += 1
            
            logger.error("No se pudo conectar con el servidor Django")
            self.server_error.emit("No se pudo conectar con el servidor Django")
            return False
            
        except Exception as e:
            logger.error(f"Error al iniciar el servidor Django: {str(e)}")
            self.server_error.emit(str(e))
            return False
    
    def _run_server(self, cmd):
        """Método interno para ejecutar el servidor en un hilo separado"""
        try:
            # Iniciar el proceso
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            self.is_running = True
            
            # Leer la salida del proceso
            while self.is_running:
                output = self.process.stdout.readline()
                if output:
                    logger.debug(f"Servidor: {output.strip()}")
                
                # Verificar si el proceso sigue en ejecución
                if self.process.poll() is not None:
                    self.is_running = False
                    break
                
                time.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Error en el hilo del servidor: {str(e)}")
            self.is_running = False
    
    def stop_server(self):
        """Detiene el servidor Django."""
        if self.process is not None:
            self.process.terminate()
            self.process.wait()
            self.process = None
            logger.info("Servidor Django detenido")
            self.server_stopped.emit()
    
    def is_server_running(self):
        """Verifica si el servidor Django está en ejecución."""
        if self.process is None:
            return False
        
        try:
            response = requests.get(f"{self.server_url}/api/health/")
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False 