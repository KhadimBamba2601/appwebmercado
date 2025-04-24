from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QStackedWidget, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Mercado Laboral")
        self.setMinimumSize(1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Barra de navegación
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)
        
        # Botones de navegación
        self.btn_ofertas = QPushButton("Ofertas de Empleo")
        self.btn_habilidades = QPushButton("Habilidades")
        self.btn_usuarios = QPushButton("Usuarios")
        
        for btn in [self.btn_ofertas, self.btn_habilidades, self.btn_usuarios]:
            btn.setMinimumHeight(40)
            btn.setFont(QFont("Arial", 10))
            nav_layout.addWidget(btn)
        
        nav_layout.addStretch()
        main_layout.addLayout(nav_layout)
        
        # Contenedor de páginas
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # Estado
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Conectar señales
        self.btn_ofertas.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_habilidades.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_usuarios.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        
        # Estilo
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QLabel {
                color: #333333;
            }
        """)

    def show_message(self, title, message, icon=QMessageBox.Icon.Information):
        QMessageBox.information(self, title, message, icon)

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_question(self, title, message):
        reply = QMessageBox.question(self, title, message,
                                   QMessageBox.StandardButton.Yes |
                                   QMessageBox.StandardButton.No)
        return reply == QMessageBox.StandardButton.Yes 