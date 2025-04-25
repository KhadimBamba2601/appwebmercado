from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from typing import Optional
from .estadisticas import EstadisticasView
from .ofertas import OfertasView
from .database import DatabaseManager

class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.setup_ui()
    
    def setup_ui(self):
        # Configuración de la ventana
        self.setWindowTitle("Gestión de Ofertas de Empleo")
        self.setMinimumSize(800, 600)
        self.setMaximumSize(1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Barra de navegación
        nav_widget = QWidget()
        nav_widget.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
            }
            QPushButton {
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:checked {
                background-color: #3498db;
            }
        """)
        
        nav_layout = QHBoxLayout(nav_widget)
        nav_layout.setContentsMargins(10, 0, 10, 0)
        nav_layout.setSpacing(5)
        
        # Botones de navegación
        self.nav_buttons = {}
        nav_items = [
            ("ofertas", "📋 Ofertas"),
            ("estadisticas", "📊 Estadísticas"),
            ("habilidades", "💻 Habilidades"),
            ("configuracion", "⚙️ Configuración")
        ]
        
        for id, text in nav_items:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, x=id: self.navigate(x))
            self.nav_buttons[id] = btn
            nav_layout.addWidget(btn)
        
        nav_layout.addStretch()
        layout.addWidget(nav_widget)
        
        # Widget apilado para el contenido
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                background-color: #f5f6fa;
            }
        """)
        layout.addWidget(self.stacked_widget)
        
        # Inicializar vistas
        self.ofertas_view = OfertasView(self.db_manager)
        self.estadisticas_view = EstadisticasView(self.db_manager)
        
        self.stacked_widget.addWidget(self.ofertas_view)
        self.stacked_widget.addWidget(self.estadisticas_view)
        
        # Seleccionar vista inicial
        self.navigate("ofertas")
    
    def navigate(self, view_id: str):
        # Desmarcar todos los botones
        for btn in self.nav_buttons.values():
            btn.setChecked(False)
        
        # Marcar el botón seleccionado
        self.nav_buttons[view_id].setChecked(True)
        
        # Cambiar a la vista correspondiente
        if view_id == "ofertas":
            self.stacked_widget.setCurrentWidget(self.ofertas_view)
        elif view_id == "estadisticas":
            self.stacked_widget.setCurrentWidget(self.estadisticas_view)
        # Aquí se agregarán más vistas cuando se implementen
    
    def show_message(self, title: str, message: str, icon: QMessageBox.Icon = QMessageBox.Icon.Information):
        """Show a message box with the given title and message"""
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()
    
    def add_content_widget(self, widget: QWidget, title: Optional[str] = None):
        """Add a widget to the content stack"""
        self.stacked_widget.addWidget(widget)
        if title:
            self.setWindowTitle(f"{title} - {self.windowTitle()}")
    
    def switch_to_widget(self, index: int):
        """Switch to the widget at the given index in the content stack"""
        self.stacked_widget.setCurrentIndex(index) 