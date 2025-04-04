import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Tareas y Mercado - Escritorio")
        self.setGeometry(100, 100, 600, 400)
        etiqueta = QLabel("Bienvenido a la app de escritorio", self)
        etiqueta.move(200, 180)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())