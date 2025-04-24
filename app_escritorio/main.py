import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ui.base_window import BaseWindow
from ui.ofertas_window import OfertasWindow
from ui.habilidades_window import HabilidadesWindow
from ui.usuarios_window import UsuariosWindow

def main():
    # Crear la aplicación
    app = QApplication(sys.argv)
    
    # Establecer estilo
    app.setStyle('Fusion')
    
    # Crear ventana principal
    window = BaseWindow()
    
    # Crear y añadir ventanas de gestión
    ofertas_window = OfertasWindow(window)
    habilidades_window = HabilidadesWindow(window)
    usuarios_window = UsuariosWindow(window)
    
    window.stacked_widget.addWidget(ofertas_window)
    window.stacked_widget.addWidget(habilidades_window)
    window.stacked_widget.addWidget(usuarios_window)
    
    # Mostrar ventana
    window.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec())

if __name__ == '__main__':
    main()