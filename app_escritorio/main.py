"""
Aplicación principal de escritorio
"""

import sys
import os
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Añadir el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.main_window import MainWindow
from config import LOG_CONFIG, UI_CONFIG

# Configuración del logging
logging.basicConfig(
    level=LOG_CONFIG['level'],
    format=LOG_CONFIG['format'],
    filename=LOG_CONFIG['file']
)

def main():
    """
    Función principal que inicia la aplicación
    """
    try:
        # Crear la aplicación Qt
        app = QApplication(sys.argv)
        
        # Configurar el estilo de la aplicación
        app.setStyle('Fusion')
        
        # Crear y mostrar la ventana principal
        window = MainWindow()
        window.setWindowTitle(UI_CONFIG['window_title'])
        window.resize(UI_CONFIG['window_width'], UI_CONFIG['window_height'])
        window.show()
        
        # Ejecutar el loop principal
        sys.exit(app.exec())
        
    except Exception as e:
        logging.error(f"Error al iniciar la aplicación: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()